#!/usr/bin/python

from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate(busnum = 1)

# Clear display and show greeting, pause 1 sec
seq = ["INITALIZING.","INITALIZING..","INITALIZING...","INITALIZING...."]

lcd.clear()
s = 0
t = 0
while True:
	lcd.message(seq[s])
	sleep(.75)
	lcd.clear()
	s += 1
	t += 1
	if (s==4):
		s = 0
	if (t==14):
		break
lcd.clear()
lcd.backlight(lcd.ON)
lcd.message("HELLO WORLD!")
# Cycle through backlight colors

sleep(2)

lcd.clear()

lcd.message("*****WARPI!*****")
