#!/usr/bin/python3

#import sys
#print(sys.path)
#import lcd
#lcd.lcdInit()

import atexit
def exit_handler():
	print('EXITING')
	GPIO.cleanup()
atexit.register(exit_handler)

import time
#for time.sleep()

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
# Using BOARD pin numbering for GPIO instead of BCM for sake of simplicity

# Callback for button press events
def btnPressed(btn):
	print('Button press detected on channel %s'%btn)

btns = [37,35,33,31,29]
# Button Numbering= UP, DOWN, LEFT, RIGHT, ENTER
for btn in btns:
	GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(btn,GPIO.FALLING,callback=btnPressed,bouncetime=200)

while True:
	time.sleep(10)
