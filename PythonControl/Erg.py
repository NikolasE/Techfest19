#!/usr/bin/env python3
# *-*- coding: utf-8 -*-

import threading
from pyrow import pyrow
from pyrow.pyrow import PyErg
import time


class Erg():
    def __init__(self):
        ergs = list(pyrow.find())
        self._erg = PyErg(ergs[0])
        self._erg_dict = {}
        self._stroke_dwelling_stamp = time.time()
        self.__last_stroke_state = -1
        self._stroke_period = 5.0
        self._erg_thread = threading.Thread(
            target=self._run_thread, daemon=True)
        self._erg_dict = self._erg.get_monitor(forceplot=True)  # populate dict
        self._erg_thread.start()

    def _run_thread(self):
        while True:
            self._erg_dict = self._erg.get_monitor(forceplot=True)
            stroke_state = self._erg_dict['strokestate']
            if 'strokestate' in self._erg_dict.keys() and stroke_state == 3 and self.__last_stroke_state == 2:
                now = time.time()
                period = now - self._stroke_dwelling_stamp
                # if period > 1.0:
                if True:
                    self._stroke_period = period
                    self._stroke_dwelling_stamp = now
            self.__last_stroke_state = stroke_state

    def get_distance(self):
        return self._erg_dict['distance']

    def get_current_stroke_complete_percent(self):
        current_stroke_elapsed_time = time.time() - self._stroke_dwelling_stamp
        return current_stroke_elapsed_time / self._stroke_period

