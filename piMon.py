#!/usr/bin/python
# does not give complete path: !/usr/bin/python3

#import sys
#print(sys.path)
#to check the path was correct

import subprocess
p = subprocess.Popen(['hostname', '-I'], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
IP, err = p.communicate()

from wireless import Wireless
wireless = Wireless()
ssid = wireless.current()

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

import Adafruit_DHT
sensor = Adafruit_DHT.DHT11
pin = 17
def dht11(delay):
	while True:
		time.sleep(delay)
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

def dsb1820(delay):
	while True:
		time.sleep(delay)
		tfile = open("/sys/bus/w1/devices/28-031574561eff/w1_slave")
		text = tfile.read()
		tfile.close()
		temperature2_data = text.split()[-1]
		temperature2 = float(temperature2_data[2:])
		temperature2 = temperature2 / 1000

#http://www.tutorialspoint.com/python/python_multithreading.htm
import thread

try:
	thread.start_new_thread( dht11,   (15) )
	thread.start_new_thread( dsb1820, (15) )
except:
	print "Error: unable to start thread"

import lcd
x=0
y=8
lcd.Init()
lcd.Print(x,y*0, ssid)
lcd.Print(x,y*1, IP)
lcd.Print(x,y*2, dt.datetime.now().strftime('%d/%m')+' - '+dt.datetime.now().strftime('%H:%M'))

while True:
	time.sleep(15)
