#! /usr/bin/python

import serial
from time import time
from LEDController.ledcontroller import LedController


name = '/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'
ser = serial.Serial(name, baudrate=230400)

lc = LedController()

last_led = 0

mm2led = 1000/60.0

g = [0, 255, 0, 0]
b = [0, 0, 255, 0]

cnt = 0

while True:
    data = ser.readline()  # .strip()#[:-2] #the last bit gets rid of the new-line chars
    if data:
        # print(data)
        s = str(data)[2:][:-5]
        try:
            trans = float(s)
        except ValueError:
            continue
        # print(trans)
        mm = trans*0.03 + 200
        current_led = int(mm / mm2led)


        if cnt % 10 != 0:
            continue


        print(mm, current_led)

        if current_led == last_led:
            continue

        if current_led > last_led:
            lc.set_led(current_led, g)
            lc.set_led(last_led, b)
        else:
            lc.set_led(current_led, b)
            lc.set_led(last_led, g)

        last_led = current_led
