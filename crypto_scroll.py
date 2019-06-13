#!/usr/bin/env python

#gilemon 2019
#can easily add this script into you crontab to autostart usinG:
#*/2 * * * * /usr/bin/python3 /home/pi/full_path_to_the_script/crypto_scroll.py

import threading
import json
from subprocess import check_output
import time
import sys
import psutil
import os
import signal
import sys

#see doc at https://www.cryptonator.com/api
apiurl = "https://api.cryptonator.com/api/ticker/"
#Base - Base currency code list (ltc/xrp/dgb/iot)
bases = ["btc", "dash", "eth"]
# Target - Target currency code (eur/usd)
target = "eur"

# Polling interval (seconds). cryptonator API accounts allow only for a certain amount of calls/day, so min interval of 600 (every 10 min)
POLL_INTERVAL = 600
ALIVE_INTERVAL = 50
ALIVE_FILE_PATH = "/tmp/crypto_scroll"
#higher the brighter
BRIGHTNESS = 0.2
#lower the faster
SCROLL_SPEED = 0.04

def autoscroll(event, basesp=["btc"], interval=0.1, ink=0):
    """Cryptocurrencies utoscroll with a thread (recursive function).
    Automatically show and scroll the buffer according to the interval value.
    :param interval: Amount of seconds (or fractions thereof), not zero
    """
    ink += 1
    if event.is_set():
        # termination code; clear the display
        scrollphathd.clear()
        scrollphathd.show()
        print("Exiting autoscroll....")
        return
    if not (int(time.time()) % POLL_INTERVAL):
        scrollphathd.clear()
        print("Updating write_string")
        scrollphathd.write_string(getCryptocurrencies(basesp), y=Y_PADDING, font=FONT, brightness=BRIGHTNESS)
        
    if (ink == ALIVE_INTERVAL):
        ink = 0
        f = open(ALIVE_FILE_PATH,"w+")
        f.write(str(int(time.time())))
        f.close()
    try:
        # Start a timer
        threading.Timer(interval, autoscroll, [event, basesp, interval, ink]).start()
        # Show the buffer
        scrollphathd.show()
        # Scroll the buffer content
        scrollphathd.scroll()
    except (KeyboardInterrupt, SystemExit):
        print("Exiting.... youhu!")
        

def getCryptocurrencies(basesp=["btc"]):
    # get Cryptocurrencies exchange rates
    scrolltext = ""
    for base in basesp:
        url = apiurl + base + "-" + target
        print("Reading: " + url )
        output = check_output(['/usr/bin/curl', url])
        print(output)
        values = json.loads(output.decode('utf-8'))
        price = int(float(values['ticker']['price']))
        print("Retrieved: " + str(price))
        scrolltext = scrolltext + "~1" + base.upper() + "=" + target.upper() + str(price)
    return scrolltext

def checkIfProcessRunning(processName):
    pcount = 0
    pids = ''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            if os.getpid() != proc.pid:
                # Check if process name contains the given name string.
                #print(proc.pid)
                here = False
                cmdline = proc.cmdline()
                if processName.lower() in proc.name().lower():
                    here = True
                if processName.lower() in cmdline:
                    here = True
                for line in cmdline:
                    line = os.path.basename(os.path.normpath(line))
                    if processName.lower() in line:
                        here = True
                if here:
                    pcount += 1
                    pids += str(proc.pid) + " "
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    if pcount > 0:
        return pids
    return False;
    
def checkIfProcessAlive():
    if os.path.exists(ALIVE_FILE_PATH):
        nowInt = int(time.time())
        print(int(time.time()))
        f = open(ALIVE_FILE_PATH, "r") 
        aliveFileVal = int(f.read())
        print(aliveFileVal)
        f.close()
        if nowInt > aliveFileVal + 10:
            print("Seems like the crypto_scroll thread went AWOL?")
            return False
        print("All is good :)")
        return True
    return False
  
my_script_name = os.path.basename(__file__)
print("My name is: " + my_script_name)

# Comment the below if you do not want to check if this script is already running
isRunning = checkIfProcessRunning(my_script_name)
#print(isRunning)
if isRunning:
    if checkIfProcessAlive():
        sys.exit('A ' + my_script_name + ' process is already running')
    else:
        print("Let's clear it and start again")
        cmd = 'kill -9 ' + isRunning
        check_output(cmd, shell=True)
        
import scrollphathd
from scrollphathd.fonts import font3x5, font5x5, font5x7, font5x7smoothed
#possible font3x5, font5x5, font5x7 (default), font5x7smoothed, font5x7unicode
FONT = font5x7
Y_PADDING = 0
if FONT.__name__ == "scrollphathd.fonts.font3x5" or FONT.__name__ == "scrollphathd.fonts.font5x5" :
    Y_PADDING = 1
if FONT.__name__ == "scrollphathd.fonts.font5x7smoothed":
    BRIGHTNESS += 0.2

# Comment the below if your display is upside down
#   (e.g. if you're NOT using it in a Pimoroni Scroll Bot)
scrollphathd.rotate(degrees=180)
# Auto scroll using a thread
scrollphathd.write_string(getCryptocurrencies(bases), y=Y_PADDING, font=FONT, brightness=BRIGHTNESS)
event = threading.Event()
autoscroll(event, bases, SCROLL_SPEED)

def signal_term_handler(signal, frame):
    print('got SIGTERM')
    scrollphathd.clear()
    scrollphathd.show()
    print("Exiting autoscroll....")
    sys.exit(0)
 
signal.signal(signal.SIGTERM, signal_term_handler)
    
while True:
    try:
        #print("all is good")
        time.sleep(0.2)
    except (KeyboardInterrupt, SystemExit):
        print("Caught the kill -2 in the main thread :)")
        event.set()
        time.sleep(0.2)
        sys.exit("Oy!")

print("Main thread exited")
