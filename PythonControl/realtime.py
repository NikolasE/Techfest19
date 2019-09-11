#! /usr/bin/python

import serial
import os
from time import sleep, time
import threading
from pyrow import pyrow
from pyrow.pyrow import PyErg
import json
import numpy as np
from VideoControl import VideoControl
import os
run_thread = True

all_data = list()

cnt_rot = 0
cnt_trans = 0
cnt_erg = 0
cnt_image = 0

do_beep = False

vc = VideoControl()

# seq_name = input("name for sequence: ")
# print(seq_name)

#
# t = int(time())
# run_name = "%s_%i" % (seq_name, t)
# folder = '/tmp/%s/' % run_name
# os.mkdir(folder)

min_gripper = 0
current_gripper = 0
gripper_front_pos = 0

def RotationThread():
    global cnt_rot, current_gripper, min_gripper, gripper_front_pos
    name = '/dev/serial/by-id/usb-SEGGER_J-Link_000599005480-if00'
    ser = serial.Serial(name, baudrate=115200)
    print(ser.is_open)

    rots = list()

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

            rot_m = rot*0.00246219 * 100
            cnt_rot += 1
            if cnt_rot % 10 != 0:
                continue
                print("%.2f" % (rot_m))
            # continue

            current_gripper = rot_m
            rots.append(rot_m)

            if len(rots) < 5:
                continue

            a = rots[-3]
            b = rots[-2]
            c = rots[-1]

            # print("%.2f, %.2f, %.2f" % (a, b, c))

            if a < b and b > c and abs(a-b) > 0.04:
                print ("XXXXXXXXXXXX MAXIMUM DETECTED at %i" % int(time()))
                # print("%.2f < %.2f > %.2f" % (a, b, c))
                min_gripper = c
                if do_beep:
                    os.system("beep -f 1000 -l 50")

            if a > b and b < c and abs(a - b) > 0.04:
                print("000000000000000000 Minimum at %i: %.1f" % (int(time()), c))
                # print("%.2f < %.2f > %.2f" % (a, b, c))
                gripper_front_pos = c
                if do_beep:
                    os.system("beep -f 1000 -l 50")

            # print(a, b, c)

    ser.close()


def TranslationThread():
    global cnt_trans, current_gripper, min_gripper
    name = '/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0'
    ser = serial.Serial(name, baudrate=230400)

    back = False

    all_trans = list()
    last_stamp = None
    stop_pos = 0
    stop_stamp = None

    front_stop = False
    front_stop_pos = 0
    front_stop_stamp = 0

    while run_thread:
        data = ser.readline()
        cnt_trans += 1
        if data:
            s = str(data)[2:][:-5]
            try:
                trans = float(s)
            except ValueError:
                continue

            trans = 0.03*trans/10 + 20
            if cnt_trans % 20 != 0:
                continue

            # print(trans)

            all_trans.append(trans)

            if len(all_trans) < 5:
                continue

            a = all_trans[-3]
            b = all_trans[-2]
            c = all_trans[-1]

            # print("%.2f, %.2f, %.2f" % (a, b, c))
            # print(c)
            v = c-b
            if c < 50:
                if back: # already stooped, waiting for acceleration:
                    # print("back: v: %.1f" % v)
                    if c > stop_pos + 5:  #v > 0.1:
                        dt_ms = (time()-stop_stamp)*1000.0
                        print("Moving FORWARD AGAIN after %.0f ms" % dt_ms)

                        gripper_dist = min_gripper - current_gripper
                        print("Gripper moved: %.1f (min: %.1f, current: %.1f" % (gripper_dist, min_gripper, current_gripper))
                        if min_gripper > 0 and gripper_dist < 500:
                            # os.system("beep -f 20 -l 300")
                            vc._say("Arms away")
                            # os.system("beep -f 200 -l 100")
                            # os.system("beep -f 100 -l 100")
                        if do_beep:
                            os.system("beep -f 900 -l 100")
                        back = False
                else:
                    # Not yet stopped:
                    # print("front yet? %.2f" % v)
                    # print()
                    if 0 > v > -0.5:
                        print("XXXXXXXXXXXXXXXXXXx BACKWARDS, STOPPING")
                        if do_beep:
                            os.system("beep -f 600 -l 100")
                        stop_pos = c
                        stop_stamp = time()
                        back = True


            # shooting the slide:
            if front_stop_pos > 0:
                # we are on the way back:
                if front_stop_pos - c > 20:
                    gripper_travel = (current_gripper - gripper_front_pos)/10.0  # to cm
                    print("00000000000000000000000000000000000000000000000000 Grpper travel: %i" % (int(gripper_travel)))
                    front_stop_pos = 0
                    if gripper_travel < 12:
                        vc._say("slide!")

            if c > 50:
                # print(v)

                if not front_stop:
                    if 0 < v < 1.0:
                        print("Front Stop")
                        front_stop = True
                        front_stop_pos = c
                        front_stop_stamp = time()
                        if do_beep:
                            os.system("beep -f 200 -l 100")
                else:
                    # we stopped, waiting for moving back:
                    if c < front_stop_pos - 3:
                        dt = (time()-front_stop_stamp)*1000.0
                        print("Moving back after %.1f ms" % dt)
                        front_stop = False
                        if do_beep:
                            os.system("beep -f 700 -l 100")


                #     if last_stamp and time()-last_stamp < 0.6:
                #         print("DT", time()-last_stamp)
                #         continue
                #
                #     print("Auslage")
                #     last_stamp = time()
                #     os.system("beep -f 200 -l 200")

            # print("%.1f" % (c-b))
            # if a < b and b > c and abs(a-b) > 0.04:
            #     print ("XXXXXXXXXXXX MAXIMUM DETECTED at %i" % int(time()))
            #     print("%.2f < %.2f > %.2f" % (a, b, c))
            #     os.system("beep -f 200 -l 200")
            #
            # if a > b and b < c and abs(a - b) > 0.04:
            #     print("000000000000000000 at %i" % int(time()))
            #     print("%.2f < %.2f > %.2f" % (a, b, c))
            #     os.system("beep -f 700 -l 200")

            # now = time()
            # msg = "T, %f, %.0f" % (now, trans)
            # all_data.append([now, msg])
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

def CameraThread():
    global cnt_image
    cap = cv2.VideoCapture(1)
    while run_thread:
        # Capture frame-by-frame
        ret, frame = cap.read()
        t = time()
        img_path = folder + 'img_%f.png' % t
        cnt_image += 1

        cv2.imwrite(img_path, frame)


threads = list()
threads.append(threading.Thread(target=RotationThread, daemon=True))
threads.append(threading.Thread(target=TranslationThread, daemon=True))
# threads.append(threading.Thread(target=ErgThread, daemon=True))
# threads.append(threading.Thread(target=CameraThread, daemon=True))
#
for t in threads:
    t.start()
#
while True:
    sleep(40)
run_thread = False
#
# print("Rot: %i, Trans: %i, Erg: %i, Images: %i" % (cnt_rot, cnt_trans, cnt_erg, cnt_image))
#
# all_data = sorted(all_data, key=lambda d: d[0])
#
#
#
# print("Writing to %s" % folder)
#
# f_r = open(folder + 'rotation.txt', 'w')
# f_t = open(folder + 'translation.txt' , 'w')
# f_e = open(folder + 'ergo.txt', 'w')
#
# f_merge = open(folder + 'all_%s.txt' % run_name, 'w')
#
# for m in all_data:
#     msg = m[1]
#     f_merge.write(msg+'\n')
#     if msg[0] == 'R':
#         f_r.write(msg+'\n')
#     if msg[0] == 'T':
#         f_t.write(msg + '\n')
#     if msg[0] == 'E':
#         f_e.write(msg + '\n')
#     f_merge.write(msg+'\n')
#
# f_r.close()
# f_t.close()
# f_e.close()
