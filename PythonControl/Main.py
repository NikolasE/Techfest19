#!/usr/bin/env python3
# *-*- coding: utf-8 -*-

import time
from VideoControl import VideoControl
from Erg import Erg
from Rotation import Rotation
from Seat import Seat
from LedController import LedController
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)


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
dist_per_time_needed = 5000 / 3600

last_seat_led = 0
last_chain_led = 0
last_speed_led = 0
last_speed = 0
last_dist_leds = 0
while True:

    # seat position
    seat_mm = seat.get_mm()
    current_led = round(valmap(seat_mm, 0, 1000, 0, 60))
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
    # print(dist, dist_expected)
    dist_leds = round(valmap(dist - dist_expected, 0, 10, 0, 60))
    if last_dist_leds != dist_leds:
        lc.set_dist(dist_leds)
        last_dist_leds = dist_leds

    # show setpoints
    percent_complete = erg.get_current_stroke_complete_percent()
    # print(percent_complete, '%, ', erg._stroke_period, 's')
    optimal_seat_mm = 500  # TODO
    optimal_seat_led = round(valmap(optimal_seat_mm, 0, 1000, 0, 60))
    lc.set_seat_setpoint(optimal_seat_led)
    optimal_chain_rotations = 5*360  # TODO
    optimal_chain_led = round(
        valmap(optimal_chain_rotations, 0, 15 * 360, 0, 60))
    lc.set_chain_setpoint(optimal_chain_led)

    time.sleep(0.05)
