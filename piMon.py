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

import threading

import Adafruit_DHT
sensor = Adafruit_DHT.DHT11
pin = 17
class dht11ThreadClass(threading.Thread):
	def __init__(self, delay):
		threading.Thread.__init__(self)
		self.delay = delay
	def run(self):
		while True:
			time.sleep(self.delay)
			global humidity, temperature
			humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
dht11Thread = dht11ThreadClass(15)
dht11Thread.start()

class ds18b20ThreadClass(threading.Thread):
	def __init__(self, delay):
		threading.Thread.__init__(self)
		self.delay = delay
	def run(self):
		while True:
			time.sleep(self.delay)
			tfile = open("/sys/bus/w1/devices/28-031574561eff/w1_slave")
			text = tfile.read()
			tfile.close()
			temperature2_data = text.split()[-1]
			global temperature2
			temperature2 = float(temperature2_data[2:])
			temperature2 = temperature2 / 1000
ds18b20Thread = ds18b20ThreadClass(15)
ds18b20Thread.start()

import lcd
class lcdThreadClass(threading.Thread):
	def __init__(self, delay):
		threading.Thread.__init__(self)
		self.delay = delay
	def run(self):
		while True:
			time.sleep(self.delay)
			x=0
			y=8
			lcd.Init()
			lcd.Print(x,y*0, ssid)
			lcd.Print(x,y*1, IP)
			lcd.Print(x,y*2, dt.datetime.now().strftime('%d/%m')+' - '+dt.datetime.now().strftime('%H:%M'))
			lcd.Print(x,y*3, 'T1=' + "{:.1f}".format(temperature) + ' - T2=' + "{:.1f}".format(temperature2))
			lcd.Print(x,y*4, 'H1=' + "{:.1f}".format(humidity))
lcdThread = lcdThreadClass(15)
lcdThread.start()

while True:
	time.sleep(15)
