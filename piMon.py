#!/usr/bin/python
# does not give complete path: !/usr/bin/python3

#import sys
#print(sys.path)
#to check the path was correct

import subprocess
p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
IP, err = p.communicate()

import atexit
def exit_handler():
	print('EXITING')
	GPIO.cleanup()
atexit.register(exit_handler)

import time
#for time.sleep()

import datetime as dt

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
# Wanted to use BOARD pin numbering for GPIO instead of BCM
# for sake of simplicity, but the Adafruit Nokia LCD Library uses BCM
led = 21
buzzer = 16
GPIO.setup(led,    GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

# Callback for button press events
def btnPressed(btn):
	GPIO.output(led,1)
	GPIO.output(buzzer,1)
	time.sleep(0.010)
	GPIO.output(buzzer,0)
	GPIO.output(led,0)
	print('Button press detected on channel %s'%btn)

btns = [26,19,13,6]
# Button Numbering= UP, DOWN, LEFT, RIGHT, ENTER
for btn in btns:
	GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(btn,GPIO.FALLING,callback=btnPressed,bouncetime=250)

import lcd
x=0
y=8
lcd.Init()
lcd.Print(x,y*0, IP)
lcd.Print(x,y*1, dt.datetime.now().strftime('%m/%y')+'   '+dt.datetime.now().strftime('%H:%M'))

while True:
	time.sleep(10)
