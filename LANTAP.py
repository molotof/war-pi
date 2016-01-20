#!/usr/bin/python
# Example using a character LCD plate.
import math
import time
import subprocess
import os

import Adafruit_CharLCD as LCD


# Initialize the LCD using the pins 
lcd = LCD.Adafruit_CharLCDPlate()

#clear display
lcd.clear()

#build list of menu options
menu = [' single int tap ', '  bridged tap  ', '  evilTwin AP  ', '  tor hotspot  ', '    poweroff    ']

# set color
lcd.set_color(0.0, 0.0, 1.0)

lcd.message('initializing\npwnPI boot seq')

lcd.show_cursor(True)
lcd.blink(True)

time.sleep(2.0)
lcd.clear()

lcd.message('pwnPI boot seq\n......completed')

time.sleep(2.0)
lcd.clear()

lcd.message('checking disk')

time.sleep(2.0)
lcd.clear()

lcd.message('checking disk\n...done')

time.sleep(2.0)
lcd.clear()

lcd.message('checking net ints')

time.sleep(2.0)
lcd.clear()

lcd.message('checking net ints\n...done')

time.sleep(2.0)
lcd.clear()

lcd.set_color(1.0, 1.0, 0.0)

lcd.message('**PwnPI READY**\nSELECT to start')

menu_index = len(menu)
menu_ptr = 0

while True:
	if lcd.is_pressed(LCD.SELECT):
		lcd.clear()
		lcd.message('   Main Menu   \nU + D to scroll')
		break
		
while True:
	if lcd.is_pressed(LCD.UP):
		if(menu_ptr < menu_index-1):
			menu_ptr=menu_ptr+1
		else:
			menu_ptr=0

		lcd.clear()
		lcd.message(menu[menu_ptr])
	if lcd.is_pressed(LCD.DOWN):
		if(menu_ptr == 0):
			menu_ptr = menu_index-1
		else:
			menu_ptr = menu_ptr-1

		lcd.clear()
		lcd.message(menu[menu_ptr])	
	if lcd.is_pressed(LCD.SELECT):
		lcd.clear()
		lcd.message(menu[menu_ptr] + '\n  * selected *  ')	
		break
if(menu_ptr == 0):
	lcd.clear()
	lcd.set_color(1.0, 0.0, 0.0)
	lcd.message('SNIFFING PACKETS')
	
#	os.popen('python /home/pi/scripts/sniffer_helper.py', "r")
	
	ps = subprocess.Popen(['sudo', 'sh', '/home/pi/scripts/start_single_tap.sh'])

	char_index = 0
	star_str = 'SNIFFING PACKETS\n'


	while True:
		if lcd.is_pressed(LCD.SELECT):
			print("EXITING")
			subprocess.call(["sudo", "pkill", "tcpdump"])
			ps.terminate()
			subprocess.call(["capinfos","/home/pi/warpi/captures/current.pcapng", "|", "grep", "'Number of packets:'", ">", "tmp_output"])		
		
		
		if(char_index >= 15):
			char_index = 0
			lcd.clear()
			star_str = 'SNIFFING PACKETS\n'
		else:
			star_str += '*'
			char_index += 1 	
		
		print(star_str)	
		#lcd.clear()	
		lcd.message(star_str)
		
		time.sleep(0.5)
