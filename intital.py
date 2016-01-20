    #wardrive
    #This is a Python script that controls the leds on a
    #Berryclip connected to the GPIO header on a
    #Rasberry Pi model B.
    #It checks if kismet_server and gpsd is running,and controlls LED1 and LED2 accordingly.
    #It also does upload the logfiles if the switch
    #connected to pin 26/GPIO07 is momentarily toggled.
    #Notes:
    #WARNING! wardriving may not be legal in your country, so CHECK THE LOCAL LAWS!
    #Your wlan node must be in reach, and have a good stable signal for upload to work!
    #wpa_supplicant.conf must be configured correctly!
    #The name of the wlan interface you are using must be correct, its normally wlan0.
    #kimset_server or kismet and gpsd must be auto-started at boot.
    #kismet_server must be configured correctly,running as SUID and log to netxml and gpsxml.
    #A GPS reciver that is compatilble with gpsd must be connected to one of the USB ports.
    #A usb wlan dongle that is supported in Debian/linux must be connected with USB.
    #Anyone can improve this script and correct it,if they share it with the rest of the world.
    #
    #
    #The Berryclips pinout is:
    #LED 1 - Pin 7 - GPIO4
    #LED 2 - Pin 11 - GPIO17
    #LED 3 - Pin 15 - GPIO22
    #LED 4 - Pin 19 - GPIO10
    #LED 5 - Pin 21 - GPIO9
    #LED 6 - Pin 23 - GPIO11
    #Buzzer - Pin 24 - GPIO8
    #Switch - Pin 26 - GPIO7
    #To do: Implement flashing of LED6 every time kismet detects a WLAN packet. I dont have the
    #knowledge of how to do that.
    #Perhaps via kismets tuntap interface ?
    #Implement controll of LED3, if the gps connected to gpsd has a position fix.
    #Sadly my knowledge of python is extremely small.
    import RPi.GPIO as GPIO
    import os
    import subprocess
    import gps
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(4, GPIO.OUT)#LED1 KISMET.
    GPIO.setup(22, GPIO.OUT)#LED3 GPS position fix
    GPIO.setup(17, GPIO.OUT)#LED2 GPSD running.
    GPIO.setup(9, GPIO.OUT)#LED5 Upload in progress.
    GPIO.setup(26, GPIO.IN)#Data upload switch,momentarily toggle.
    #Makes sure all LED's are at the same state initially (off):
    GPIO.output(4, True)
    GPIO.output(17, True)
    GPIO.output(22, True)
    GPIO.output(9, True)
    GPIO.output(10, True)
    while 1 < 2:
       kismet = subprocess.Popen(['ps -ef | grep kismet_server'])#checks if kismet_server is running.
       stdout = subprocess.PIPE, shell=True() #Assigns the output from the grep to the kismet variable.
       (output, error) = kismet.communicate()
       if 'kismet_server' in output: GPIO.output(4, False) #Turn on KISMET LED
    else:
       GPIO.output(4, True) #Turn off KISMET LED.
       gps = subprocess.Popen(['ps -ef | grep gpsd'],
       stdout = subprocess.PIPE, shell=True)#Assigns the output from the grep to the gps variable
       (output, error) = gps.communicate()
       if 'gpsd' in output: GPIO.output(17, False) #Turn on GPSD LED.
       else:
          GPIO.output(17, True) #Turn off GPSD LED
    #Button snippet,connects to your wlan node,and stops kismet_server,also uploads the logfiles to wigle.net
    while True:
       if (GPIO.input(26)):
          time.sleep(0.05)#Button debounce.
          os.system('killall kismet')#stops all instances of kismet.
          os.system('killall kismet_server')#stops all instances of kismet_server.
          time.sleep(2)# added so kismet has the time to die.      
          os.system('/etc/init.d/networking restart')#restarts networking
          time.sleep(1.5)#wait for networking to restart.
          os.system('wpa_supplicant -i wlan0 -c /etc/wpa_supplicant.conf')#connects to your wlan node.
          time.sleep(10)#added so wlan0 has time to autenticate and assosiate with the wlan node.
          command = os.system('ping -c 5 http://www.wigle.net')#checks if wigle.net is up.
          if command == 0: print "wigle.net is up."
    #This metod of uploading the logfiles to wigle.net works, but it is perhaps a bit ackward.
       os.system('mv path/to/kismet-logs/*.gpsxml /path/to/kismet-logs/upload.gpsxml')#renames the gpsxml file so the curl command can use it,because the curl command does not support wildcards.
       os.system('mv /pathto/kismet-logs/*.netxml /pathto/kismet-logs/upload.netxml')#renames the gpsxml file so the curl command can use it,because the curl command does not support wildcards.
       os.system('curl -F observer=your-wigleusername -F password=your-password -F stumblefile=@/pathto/kismet-logs/upload.gpsxml -F Send=Send https://wigle.net/gps/gps/main/confirmfile/')#uploads the gpsxml file.
       time.sleep(17)#waits 17 seconds so the upload has time to complete,perhaps there is a more elegant solution?
       os.system('curl -F observer=your-wigle.username -F password=your-password -F stumblefile=@/path-to/kismet-logs/upload.netxml -F Send=Send https://wigle.net/gps/gps/main/confirmfile/')#uploads the gpsxml file.
       time.sleep(17)#waits 17 seconds so the upload has time to complete,perhaps there is a more elegant solution?
       #removes the uploaded log files:
       os.system('rm /path-to/kismet-logs/*.gpsxml')
       os.system('rm /path-to/kismet-logs/*.netxml')
       command = os.system('ifconfig wlan0 down')#disables the wireless interface, i think thats a "ugly" way to disconnect.
       command = os.system('dhclient -r wlan0')#Releases the DHCP IP.
       command = os.system('ifconfig wlan0 up')#turns the interface back on, so kismet can access it.
       time.sleep(1.5)#pause so wlan0 has time to come up.
       command = os.system('kismet_server')#restarts kismet_server to resume scanning.
       GPIO.output(9, False)#Turns off LED5.
    else:
          print "Wigle.net is down."
