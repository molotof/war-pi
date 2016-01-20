#!/usr/bin/python

##***IMPORTS***##
import os, re
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
##***END IMPORTS***##

##***BEGIN STARTUP PAGENTRY***##
# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()

# Clear display and show greeting, pause 3 sec
lcd.clear()
lcd.backlight(lcd.RED)
lcd.message("Welcome to the..\n{Raspberry Pwn!}")
sleep(5)
#lcd.backlight(lcd.ON)

#show options
lcd.clear()
lcd.message("loading...")
sleep(5)
lcd.clear()
lcd.message("drivers loaded\ndevice ready")
sleep(4)
lcd.clear()
lcd.message("{Raspberry Pwn!}\n   Main Menu   ")

# Cycle through backlight colors
col = (lcd.OFF , lcd.YELLOW, lcd.GREEN, lcd.TEAL,
       lcd.BLUE, lcd.VIOLET, lcd.RED   , lcd.GREEN)
for c in col:
    lcd.backlight(c)
    sleep(.5)
##***END STARTUP PAGENTRY***##

##***GLOBAL VARIABLES***##
#button assignments
btn = ((lcd.LEFT),
       (lcd.UP),
       (lcd.DOWN),
       (lcd.RIGHT),
       (lcd.SELECT))
choice=5
exitList=[5]
exitSeq=['4','3','2','1']
shutdownSeq=['1','4','1','4']
restartSeq=['1','4','2','3']
lcdChars=15
##***END GLOBAL VARIABLES***##
#scan for APs and write results to logfile
def wapScanning():
	lcd.clear()
	lcd.message("scanning for\n access points")
	##DONT FORGET TO UNCOMMENT TO RUN!#
	os.system("iwlist wlan0 scan > result")
	lcd.clear()
	lcd.message("scanning complete")
	aps = readfile()
	showaps(aps)
	return		
#show list of APs found			
def showaps(list):
	lcd.clear()
	count = 0
	size = len(list)
	#display # of APs found
	if not list[0]:		
		lcd.clear()
		lcd.message("No Wireless APs\nfound!")
		sleep(3)
		printmain()
		return
	lcd.clear()
	tmp1 = str(size)
	tmp2 = tmp1 + ' Wireless AP(s)\nFound'
	lcd.message(tmp2)
	while True:
		for b in btn:
			#cycle using up+down buttons
			if lcd.buttonPressed(b):
				if b==2 or b==3:
 					temp_list=list[count]
					essid=temp_list[0]
					sig=temp_list[1]
					enc="WPA2"
					temp_list.append("WPA2")
					lcd.clear()
					lcd.message(essid + "\nS:" + sig + " E:" + enc )
					sleep(1.4)
					scroll(temp_list)
					count+=1
					#loop through list of APs
					if count >= size:
						count=0
				elif b==4:
					lcd.clear()
					printmain()
					sleep(3)
					main()			
#read in AP scanner logfile
def readfile():
	logfile = open("result", "r").readlines()
	aps = []
	data = []
	linect = 0
	for line in logfile:
		if re.search("Cell", line):
			data = filter(None, data)
			aps.append(data)
			data = []
		else:
			line = line.lstrip()
			data.append(line)		
	#save last dataset
	data=filter(None,data)
	aps.append(data)
	aps = filter(None, aps)
	aps = processData(aps)
	return aps

def processData(list):
	singleAP=[]
	allAP = []
	for data in list:
		oneap = list.pop()
		for el in oneap:
			#Pull ESSID, remove crap around it
			ssid=re.findall(r'"(.*?)"',el)
			essid=str(ssid)
			essid=essid[2:len(essid)]
			essid=essid[0:len(essid)-2]
			singleAP.append(essid)
			#Search for quality/signal
			if re.search("^Quality", el):
				#split on = 
				temp=re.split("=",el)
				sig=temp[len(temp)-1]
				m=re.search("\n",sig)
				#get rid of \n
				sig[:m.start()] + sig[m.end():]
				#write to single AP list
				singleAP.append(sig[:7])
			#singleAP.append(re.findall
		singleAP=filter(None,singleAP)
		allAP.append(singleAP)
		singleAP = []
	return allAP
				


#print main menu greeting
def printmain():
	lcd.clear()
	lcd.message("{PWNIE EXPRESS!}\n   Main Menu  ")
#print not implemented message
def printNI():
	lcd.clear()
	lcd.message("Not Implemented\n      :-(")
	sleep(3)
	printmain()

#get rid of the duplicate chars
def trim_input(b):
	string_b=str(b)
	#take only first # from button press
	trimed=string_b[:1]
	#if last # in breadcrumbs
	#is different then button press, replace
	if exitList[len(exitList)-1]!=trimed:
		exitList.append(trimed)
	else:
		return

#check for exit button sequence
def exitCheck():
	#pull last 4 button presses
	seq=exitList[len(exitList)-4:len(exitList)]
	#compare to exit sequence
	if seq==exitSeq:
		return True
def restartCheck():
	seq=exitList[len(exitList)-4:len(exitList)]
	if seq==restartSeq:
		lcd.clear()
		lcd.message("{PWNIE EXPRESS!}\nsystem rebooting")
		sleep(5)
		os.system("reboot")
		sleep(7)
def shutdownCheck():
	seq=exitList[len(exitList)-4:len(exitList)]
	if seq==shutdownSeq:
		lcd.clear()
		lcd.message("{PWNIE EXPRESS!}\nsystem shutdown")
		sleep(5)
		os.system("poweroff")	
		os.sleep(7)

def scroll(node):
	currentDisplay=' '
	essid=node[0]
	sig=node[1]
	enc=node[2]
	chars=0
	essid=essid+"     "
	essid_char=list(essid)
	
	if len(essid_char) < 15:
		return
	elif chars <= 15 and len(essid_char)!=0:
		while chars < 15:
			currentDisplay=currentDisplay+essid_char.pop(0)
			lcd.clear()
			lcd.message(currentDisplay[1:]+"\nS:"+sig+" E:"+enc)
			chars+=1
	while True:
		for b in btn:
			if lcd.buttonPressed(b) and b==1:
				lcd.clear()
				if len(essid_char) > 1:
					currentDisplay=currentDisplay[1:]
					currentDisplay=currentDisplay+essid_char.pop(0)
					lcd.message(currentDisplay+"\nS:"+sig+" E:"+enc)
					sleep(.15)
				elif len(essid_char)==1:
					lcd.clear()
					lcd.message(" " + essid+"\nS:"+sig+" E:"+enc)
					currentDisplay=essid
					essid_char=list(essid)
			elif lcd.buttonPressed(b) and (b==2 or b==3):
				return
			elif lcd.buttonPressed(b) and b==4:
				lcd.clear()
				printmain()
				sleep(2)
				main()
#Main Program Loop
def main():
	while True:
		for b in btn:
			#wait for button press
			if lcd.buttonPressed(b):
				#breakout for button functions
				if(b==4):
					lcd.clear()
					lcd.message("WAP Scanner")			
					choice=4
					trim_input(b)
				if(b==3):
					lcd.clear()
					lcd.message("Rogue AP")				
					choice=3
					trim_input(b)
				if(b==2):
					lcd.clear()
					lcd.message("WEP Cracker")				
					choice=2
					trim_input(b)
				if(b==1):
					lcd.clear()
					lcd.message("WPS Scanner")
					choice=1
					trim_input(b)
				#deal with 'select' button press
				if(b==0):
					#check if exit sequence was entered
					restartCheck()
					shutdownCheck()
					if exitCheck():
						lcd.clear()
						lcd.message("Goodbye")
						sleep(3)
						lcd.clear()
						lcd.message("{Raspberry Pwn!}\nstanding by.....")
						exit()
					elif choice==4:
						wapScanning()
					elif choice==3:
						printNI()
					elif choice==2:
						printNI()
					elif choice==1:
						printNI()

#main program
main()
