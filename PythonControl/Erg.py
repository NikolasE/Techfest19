#!/usr/bin/env python3
# *-*- coding: utf-8 -*-

import threading
from pyrow import pyrow
from pyrow.pyrow import PyErg


class Erg():
    def __init__(self):
        ergs = list(pyrow.find())
        self._erg = PyErg(ergs[0])
        self._erg_dict = {}
        self._erg_thread = threading.Thread(
            target=self._run_thread, daemon=True)
        self._erg_dict = self._erg.get_monitor(forceplot=True)  # populate dict
        self._erg_thread.start()

    def _run_thread(self):
        while True:
            self._erg_dict = self._erg.get_monitor(forceplot=True)

    def get_distance(self):
        return self._erg_dict['distance']
