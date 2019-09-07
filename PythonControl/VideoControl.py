#!/usr/bin/env python3
# *-*- coding: utf-8 -*-

import autopy


class VideoControl():
    def __init__(self):
        pass

    def send_playpause(self):
        autopy.key.tap(autopy.key.Code.SPACE, [])


if __name__ == '__main__':
    videoControl = VideoControl()
    videoControl.send_playpause()
