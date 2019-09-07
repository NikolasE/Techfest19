#! /usr/bin/python

import serial
import os
from time import sleep, time
import threading
from pyrow import pyrow
from pyrow.pyrow import PyErg
import json

run_thread = True

all_data = list()

cnt_rot = 0
cnt_trans = 0
cnt_erg = 0

seq_name = input("name for sequence: ")
print(seq_name)

def RotationThread():
    global cnt_rot
    name = '/dev/serial/by-id/usb-SEGGER_J-Link_000599005480-if00'
    ser = serial.Serial(name, baudrate=115200)

    while run_thread:
        data = ser.readline().strip()
        if data:
            s = str(data)[2:][:-1]
            # print(s)
            spl = s.split(':')
            if len(spl) != 3:
                print("Could not parse " + s)
                continue

            try:
                speed, angle, rotations = map(float, spl)
            except ValueError as e:
                print(e)
                continue

            if angle < 0:
                angle += 360

            rot = angle + rotations*360
            # print(rot)
            # print("rad", s.split(':'))
            now = time()
            msg = "R, %f, %f, %f" % (now, speed, rot)
            all_data.append([now, msg])
            cnt_rot += 1

def TranslationThread():
    global cnt_trans
    name = '/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'
    ser = serial.Serial(name, baudrate=230400)

    while run_thread:
        data = ser.readline()#.strip()#[:-2] #the last bit gets rid of the new-line chars
        if data:
            s = str(data)[2:][:-5]
            try:
                trans = float(s)
            except ValueError:
                continue
            now = time()
            msg = "T, %f, %.0f" % (now, trans)
            all_data.append([now, msg])
            cnt_trans +=1

def ErgThread():
    global cnt_erg
    ergs = list(pyrow.find())

    erg = PyErg(ergs[0])

    while run_thread:
        erg_dict = erg.get_monitor(forceplot=True)
        now = time()
        msg = "E, %f, %s" % (now, json.dumps(erg_dict))
        all_data.append([now, msg])
        cnt_erg += 1


thread1 = threading.Thread(target=RotationThread)
thread2 = threading.Thread(target=TranslationThread)
thread3 = threading.Thread(target=ErgThread)

thread1.start()
thread2.start()
thread3.start()


sleep(10)
run_thread = False

print("Rot: %i, Trans: %i, Erg: %i" % (cnt_rot, cnt_trans, cnt_erg))

all_data = sorted(all_data, key=lambda d: d[0])

t = int(time())
folder = '/tmp/%s_%i/' % (seq_name, t)
os.mkdir(folder)

print("Writing to %s" % folder)

f_r = open(folder + 'rotation.txt', 'w')
f_t = open(folder + 'translation.txt' , 'w')
f_e = open(folder + 'ergo.txt', 'w')

f_merge = open(folder + 'all.txt', 'w')

for m in all_data:
    msg = m[1]
    f_merge.write(msg+'\n')
    if msg[0] == 'R':
        f_r.write(msg+'\n')
    if msg[0] == 'T':
        f_t.write(msg + '\n')
    if msg[0] == 'E':
        f_e.write(msg + '\n')

f_r.close()
f_t.close()
f_e.close()
f_merge.write(msg+'\n')