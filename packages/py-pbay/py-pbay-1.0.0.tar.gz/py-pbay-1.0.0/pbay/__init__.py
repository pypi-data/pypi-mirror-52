name = "py-pbay"

import sys
import time
import math
from collections import OrderedDict
import re
import serial  # pip3 install pyserial
import logging
from serial.serialutil import SerialException
from threading import Thread

INIT_VALUES = OrderedDict({
    # Board address, sequence number
    'BAD': None, 'SQN': None,

    # sensor currents
    'CMO': None, 'SO2': None, 'NO2': None, 'H2S': None,
    'OZO': None, 'IAQ': None, 'IRR': None,

    # temperatures
    'SHT': None,  'LPT': None, 'HDT': None,
    'AT0': None,  # CO ADC
    'AT1': None,  # IAQ/IRR ADC temp
    'AT2': None,  # O3/NO2 ADC temp
    'AT3': None,  # SO2/H2S ADC temp
    'LTM': None,  # CO LMP Temp

    # humidity
    'SHH': None, 'HDH': None,

    # pressure
    'LPP': None,

    # Si1145 sensor (light)
    'SIR': None, 'SUV': None, 'SVL': None,
})


class Gas(object):
    def __init__(self, name, calib_curr, calib_temp, temp_source, nanoamps_per_ppm, t_const):
        self.name = name
        self.calib_curr = calib_curr
        self.calib_temp = calib_temp
        self.temp_source = temp_source
        self.picoamps_per_ppm = 1000 * nanoamps_per_ppm
        self.t_const = t_const 

    def __str__(self):
        return self.name


class PBay(Thread):
    def __init__(self, serial_address, log_filename, gas_list):
        super(PBay, self).__init__()
        # initialize state
        self._raw = INIT_VALUES
        self._values = {}
        self._gases = gas_list
        self._is_running = False  # TODO: check if threading module doesn't already have that kind of flag

        # initialize peripherals
        self._s = serial.Serial(port=serial_address, baudrate=115200, timeout=5)
        self._p = re.compile('-?[A-Z][A-Z|0-9][A-Z|0-9]{1}=-?[0-9|A-Z]+')

        # configure logger
        self._log = logging.getLogger('pbay_driver')
        self._log.setLevel(logging.INFO)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(log_filename)
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self._log.addHandler(fh)
        self._log.addHandler(ch)

    def __enter__(self):

        # wait for first batch of _raw to come
        while None in self._raw.values():
            li = self._read_sensor()
            kv = self._parse(li)
            self._update_state(kv)

            missing_values = [k for k, v in self._raw.items() if v is None]
            self._log.info("Waiting for _raw... Still waiting for: {}".format(missing_values))

            time.sleep(.5)  # so it doesn't spin

        self._log.info("Got all the parameters. Starting.")
        self._calculate_values()
        self._is_running = True
        self.start()
        return self

    def run(self):
        while self._is_running:
            try:
                li = self._read_sensor()
                kv = self._parse(li)
                self._update_state(kv)
                self._calculate_values()
            except SerialException as e:
                self._log.critical("Device disconnected with Exception: {}".format(e))
                self._is_running = False
                # TODO: add some better error handling?
                # Chances are that it will reconnect and change /dev/tty*

    def _read_sensor(self):
        li = str(self._s.readline())
        self._log.debug("Recived a line: " + li)
        return li

    def _parse(self, data):
        keyvalue_list = self._p.findall(data)
        return keyvalue_list

    def _update_state(self, keyvalue_pairs):
        for kv in keyvalue_pairs:
            key = kv[0:3]
            if key in INIT_VALUES.keys():
                if key == 'BAD' or key == 'SQN':
                    self._raw[key] = kv[4:]
                else:
                    self._raw[key] = float(kv[4:])
            else:
                self._log.warning("Received an erronous key from the device: " + key)

    def _calculate_values(self):
        for g in self._gases:
            deltaT = self._raw[g.temp_source]/100 - g.calib_temp
            I_net = self._raw[g.name] - g.calib_temp * pow(math.e, deltaT/g.t_const)
            self._values[g.name] = I_net/g.picoamps_per_ppm
        self._log.debug("Calculated values" + str(self._values))

    def __getattr__(self, attr):
        gas_names = list(map(str, self._gases))
        if attr not in gas_names:
            raise AttributeError(
                '{} has no attribute {}.Maybe one of: {}?'.format(self, attr, gas_names))
        else:
            return self._values[attr]

    def __exit__(self, etype, value, traceback):
        self._is_running = False
        self.join()  # TODO: is this right?
        self._s.close()

    def stop(self):
        self._is_running = False
