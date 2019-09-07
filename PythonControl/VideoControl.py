#!/usr/bin/env python3
# *-*- coding: utf-8 -*-

import autopy
import pyttsx3
import threading


class VideoControl():
    def __init__(self):
        self._engine = pyttsx3.init()
        # voices = engine.getProperty('voices')
        # self._engine.setProperty('voice', voices[8].id)

    def send_play(self):
        autopy.key.tap(autopy.key.Code.SPACE, [])
        self._voice_thread = threading.Thread(target=self._say, args=("Good work. Resuming video.",))
        self._voice_thread.start()

    def send_pause(self):
        autopy.key.tap(autopy.key.Code.SPACE, [])
        self._voice_thread = threading.Thread(target=self._say, args=("Not enough rowing. Stopping video.",))
        self._voice_thread.start()

    def _say(self, text):
        self._engine.say(text)
        self._engine.runAndWait()


if __name__ == '__main__':
    videoControl = VideoControl()
    videoControl.send_playpause()
    print("done")
