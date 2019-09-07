#!/usr/bin/env python3
# *-*- coding: utf-8 -*-

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from LEDController.ledcontroller import LedController
from Seat import Seat
from Rotation import Rotation
import time


def valmap(ivalue, istart, istop, ostart, ostop):
        """
        map a value from one input range to output range, like the Arduino map function
        :param ivalue: input value to map
        :param istart: input from
        :param istop: input to
        :param ostart: output from
        :param ostop:  output to
        :return: mapped input
        """
        return ostart + (ostop - ostart) * ((ivalue - istart) / (istop - istart))



rotation = Rotation()
seat = Seat()

lc = LedController()
lc.reset_leds()

mm2led = 1000 / 60.0

last_seat_led = 0
last_chain_led = 0
last_speed_led = 0
while True:
    mm = seat.get_mm()
    current_led = int(mm / mm2led)
    if last_seat_led != current_led:
        lc.set_seat(current_led)
        last_seat_led = current_led

    rotations = rotation.get_rotation()
    chain_led = round(valmap(rotations, 0, 15*360, 0, 60))
    if last_chain_led != chain_led:
        lc.set_chain(chain_led)
        last_chain_led = chain_led

    speed = rotation.get_speed()
    speed_led = round(valmap(speed, 0, 80000, 0, 255))
    if speed > 0 and last_speed_led != speed_led:
        lc.set_vel(speed_led)
        last_speed_led = speed_led

    time.sleep(0.05)
