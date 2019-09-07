#!/usr/bin/env python3
# *-*- coding: utf-8 -*-

import serial
import threading


class Rotation():
    def __init__(self, serial_port='/dev/serial/by-id/usb-SEGGER_J-Link_000599005480-if00', baud_rate=115200):
        self._serial = serial.Serial(port=serial_port, baudrate=baud_rate)
        if not self._serial.isOpen():
            raise RuntimeError("Couldn't open %s" % serial_port)
        self.speed = 0
        self.rot = 0
        self._ser_thread = threading.Thread(
            target=self._read_thread, daemon=True)
        self._ser_thread.start()

    def _read_thread(self):
        while True:
            data = self._serial.readline().strip()
            if data:
                s = str(data)[2:][:-1]
                spl = s.split(':')
                if len(spl) != 3:
                    print("Could not parse " + s)
                    continue

                try:
                    self.speed, angle, rotations = map(float, spl)
                except ValueError as e:
                    print(e)
                    continue

                if angle < 0:
                    angle += 360

                self.rot = angle + rotations*360

    def get_speed(self):
        return self.speed

    def get_rotation(self):
        return self.rot
