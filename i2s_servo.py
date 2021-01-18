#!/usr/bin/python
# Copyright (c) 2021 Philip Company
# Author: Philip Chen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import speech_recognition as sr
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT)

def servo():
    pwm = GPIO.PWM(33, 50)
    pwm.start(2.5)              # min 2.5, max 11.5 180 degrees

    for i in range(0,3):
        pwm.ChangeDutyCycle(2.5)
        print("0 degree")
        time.sleep(1.0)
        pwm.ChangeDutyCycle(7.0)
        print("90 degree")
        time.sleep(1.0)
        pwm.ChangeDutyCycle(11.5)
        print("180 degree")
        time.sleep(1.0)
        pwm.ChangeDutyCycle(7.0)
        print("90 degree")
        time.sleep(1.0)

    pwm.start(0)

pwm = GPIO.PWM(33, 50)
pwm.start(2.5)              # min 2.5, max 11.5 180 degrees
r = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('say one of follows :\n"turn right"\n"turn left"\n"stay in the middle"\n')
        print('say "stop" to exit')
        audio = r.record(source, duration = 3)

    try:
        voice_data = r.recognize_google(audio, language='en-US')
        print(voice_data)
        if voice_data.lower() == 'turn right':
            pwm.ChangeDutyCycle(2.5)
        elif voice_data.lower() == 'stay in the middle':
            pwm.ChangeDutyCycle(7.0)
        elif voice_data.lower() == 'turn left':
            pwm.ChangeDutyCycle(11.5)
        elif voice_data.lower() == 'stop':
            pwm.start(0)
            break
    except Exception as e:
        print (e)
