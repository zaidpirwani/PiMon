#!/usr/bin/python

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import Image
import ImageDraw
import ImageFont


def Init():
	global disp, image, draw, font
	DC = 23
	RST = 24
	SPI_PORT = 0
	SPI_DEVICE = 0
	disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
	disp.begin(contrast=60)
	disp.clear()
	disp.display()

	# Make sure to create image with mode '1' for 1-bit color.
	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)
	# Draw a white filled box to clear the image.
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	# Load default font.
	font = ImageFont.load_default()
	disp.image(image)
	disp.display()
	return()

def Show():
	disp.image(image)
	disp.display()

def Print(x,y,str):
	draw.text((x,y), str, font=font)
	Show()

def Clear():
	# Draw a white filled box to clear the image.
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)	
	Show()

if __name__ == '__main__':
	print('LCD Imported')
	lcdInit()
