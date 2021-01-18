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
import time
import sys
import smbus

bus = smbus.SMBus(1)

# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# I2C LCD
# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

# send command to display (no need for external use)
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

# set display text \n for second line(or auto wrap)
def setText(text):
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count >= 16:
            count = 0
            row += 1
            if row >= 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

def i2c_lcd_test():
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)

    for i in range(0,5):
        setRGB( 255, 0, 0 )
        time.sleep(1)
        setRGB( 255, 255, 0 )
        time.sleep(1)
        setRGB( 0, 255, 0 )
        time.sleep(1)
        setRGB( 0, 255, 255 )
        time.sleep(1)
        setRGB( 0, 0, 255 )
        time.sleep(1)
        setRGB( 255, 0, 255 )
        time.sleep(1)

    setRGB( 128, 255, 0 )
    setText( "Hello world !\nIt works !\n" )

def i2c_lcd_init():
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)

i2c_lcd_init()
r = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print('say one of follows :\n"red carpet"\n"green grass"\n"navy blue"\n"yellow river"\n"blue sky"\n"pink panther"\n"snow white"\n')
        print('say "stop" to exit')
        audio = r.record(source, duration = 3)
    
    try:
        voice_data = r.recognize_google(audio, language='en-US')
        print(voice_data)
        if voice_data.lower() == 'red carpet':
            setRGB( 255, 0, 0 )
        elif voice_data.lower() == 'green grass':
            setRGB( 0, 255, 0 )
        elif voice_data.lower() == 'navy blue':
            setRGB( 0, 0, 255 )
        elif voice_data.lower() == 'yellow river':
            setRGB( 255, 255, 0 )
        elif voice_data.lower() == 'blue sky':
            setRGB( 0, 255, 255 )
        elif voice_data.lower() == 'pink panther':
            setRGB( 255, 0, 255 )
        elif voice_data.lower() == 'snow white':
            setRGB( 255, 255, 255 )
        elif voice_data.lower() == 'stop':
            setRGB( 0, 0, 0 )
            break
    except Exception as e:
        print (e)
    
