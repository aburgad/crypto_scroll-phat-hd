#!/usr/bin/env python

#gilemon 2019
#can easily add this script into you crontab to autostart usinG:
#*/2 * * * * /usr/bin/python3 /home/pi/full_path_to_the_script/crypto_scroll.py

import threading
import scrollphathd
from scrollphathd.fonts import font3x5, font5x5, font5x7, font5x7smoothed
import json
from subprocess import check_output
import time
import sys
import psutil
import os

#see doc at https://www.cryptonator.com/api
apiurl = "https://api.cryptonator.com/api/ticker/"
#Base - Base currency code list (ltc/xrp/dgb/iot)
bases = ["btc", "dash", "eth"]
# Target - Target currency code (eur/usd)
target = "eur"

# Polling interval (seconds). cryptonator API accounts allow only for a certain amount of calls/day, so min interval of 600 (every 10 min)
POLL_INTERVAL = 600
#higher the brighter
BRIGHTNESS = 0.2
#lower the faster
SCROLL_SPEED = 0.028888
#possible font3x5, font5x5, font5x7 (default), font5x7smoothed, font5x7unicode
FONT = font5x7

Y_PADDING = 0
if FONT.__name__ == "scrollphathd.fonts.font3x5" or FONT.__name__ == "scrollphathd.fonts.font5x5" :
    Y_PADDING = 1
if FONT.__name__ == "scrollphathd.fonts.font5x7smoothed":
    BRIGHTNESS += 0.2

def autoscroll(event, basesp=["btc"], interval=0.1):
    """Cryptocurrencies utoscroll with a thread (recursive function).
    Automatically show and scroll the buffer according to the interval value.
    :param interval: Amount of seconds (or fractions thereof), not zero
    """
    if event.is_set():
        # termination code; clear the display
        scrollphathd.clear()
        scrollphathd.show()
        print("Exiting autoscroll....")
        return
    if not (int(time.time()) % POLL_INTERVAL):
        scrollphathd.clear()
        scrollphathd.write_string(getCryptocurrencies(basesp), y=Y_PADDING, font=FONT, brightness=BRIGHTNESS)
    try:
        # Start a timer
        threading.Timer(interval, autoscroll, [event, basesp, interval]).start()
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
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            cmdline = proc.cmdline()
            if processName.lower() in proc.name().lower():
                pcount += 1
            if processName.lower() in cmdline:
                pcount += 1
            for line in cmdline:
                line = os.path.basename(os.path.normpath(line))
                if processName.lower() in line:
                    pcount += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    if pcount > 1:
        return True
    return False;
  
my_script_name = os.path.basename(__file__)
print("My name is: " + my_script_name)

# Comment the below if you do not want to check if this script is already running
if checkIfProcessRunning(my_script_name):
    sys.exit('A ' + my_script_name + ' process is already running')

# Comment the below if your display is upside down
#   (e.g. if you're NOT using it in a Pimoroni Scroll Bot)
scrollphathd.rotate(degrees=180)
# Auto scroll using a thread
scrollphathd.write_string(getCryptocurrencies(bases), y=Y_PADDING, font=FONT, brightness=BRIGHTNESS)
event = threading.Event()
autoscroll(event, bases, SCROLL_SPEED)
    
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
