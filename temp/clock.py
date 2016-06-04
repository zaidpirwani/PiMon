import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
up_btn = 26
down_btn = 19
left_btn = 13
right_btn = 6
GPIO.setup(up_btn,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(down_btn,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(left_btn,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(right_btn,GPIO.IN,pull_up_down=GPIO.PUD_UP)

led = 21
buzzer = 16
GPIO.setup(led,GPIO.OUT)
GPIO.setup(buzzer,GPIO.OUT)

while False:
	GPIO.output(led,1)
	GPIO.output(buzzer,1)
	time.sleep(1)
	GPIO.output(led,0)
	GPIO.output(buzzer,0)
	time.sleep(1)
	

import Adafruit_DHT
sensor = Adafruit_DHT.DHT11
pin = 17
humidity,temperature = Adafruit_DHT.read_retry(sensor, pin)

from datetime import datetime
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi hardware SPI config:
DC = 23
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0
# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Initialize library.
disp.begin(contrast=60)

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white filled box to clear the image.
draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

# Load default font.
font = ImageFont.load_default()

light = 1
clock = True
temp = 0
t = ' '
h = ' '
t2=' '
print 'Press Ctrl-C to quit.'
while True:
	if (GPIO.input(up_btn)==False):
		clock = not clock
	if (GPIO.input(left_btn)==False):
		sys.exit()
	led = not led
	GPIO.output(21,led)
	if clock:
		x = 0
		y = 8
		draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
		draw.text((x,y*0),  datetime.now().strftime(' %Y-%m-%d'), font=font)
		draw.text((x,y*1), datetime.now().strftime(' %H:%M:%S'), font=font)
		draw.text((x,y*2),' T='+t+'C H='+h+'%' , font=font)
		draw.text((x,y*3),' T2='+t2+'C' , font=font)
		temp = temp+1
		if(temp>1):
			humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
			if humidity is not None and temperature is not None:
				t = "{:.0f}".format(temperature) 
				h = "{:.0f}".format(humidity)
				tfile = open("/sys/bus/w1/devices/28-031574561eff/w1_slave")
				text = tfile.read()
				tfile.close()
				temperature2_data = text.split()[-1]
				temperature2 = float(temperature2_data[2:])
				temperature2 = temperature2 / 1000
				t2 = "{:.2f}".format(temperature2) 
			temp=0
		disp.image(image)
		disp.display()
	time.sleep(1.0)
