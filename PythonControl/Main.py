#!/usr/bin/env python3
# *-*- coding: utf-8 -*-

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from LedController import LedController
from Seat import Seat
from Rotation import Rotation
from Erg import Erg
from VideoControl import VideoControl
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

erg = Erg()

videoControl = VideoControl()

workout_start = time.time()
dist_per_time_needed = 5000/3600

last_seat_led = 0
last_chain_led = 0
last_speed_led = 0
last_speed = 0
last_dist_leds = 0
while True:

    # seat position
    mm = seat.get_mm()
    mm2led = 1000 / 60.0
    current_led = int(mm / mm2led)
    if last_seat_led != current_led:
        lc.set_seat(current_led)
        last_seat_led = current_led

    # chain position
    rotations = rotation.get_rotation()
    chain_led = round(valmap(rotations, 0, 15*360, 0, 60))
    if last_chain_led != chain_led:
        lc.set_chain(chain_led)
        last_chain_led = chain_led

    # chain speed
    speed = rotation.get_speed()
    if speed < 0:
        last_speed = 0
    speed_led = round(valmap(speed, 0, 80000, 0, 255))
    if speed > last_speed and speed > 0 and last_speed_led != speed_led:
        lc.set_vel(speed_led)
        last_speed_led = speed_led
        last_speed = speed

    # erg distance
    dist = erg.get_distance()
    dist_expected = (time.time() - workout_start) * dist_per_time_needed
    print(dist, dist_expected)
    dist_leds = round(valmap(dist - dist_expected, 0, 10, 0, 60))
    if last_dist_leds != dist_leds:
        lc.set_dist(dist_leds)
        last_dist_leds = dist_leds

    time.sleep(0.05)
