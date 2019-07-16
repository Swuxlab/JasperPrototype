import time
import inspect

from gpiozero import LED
from . import pixel_ring

import usb.core
import usb.util

power = LED(5)


def command(n):
    #turn on LED
    power.on()

    #brightness and pattern settings
    pixel_ring.set_brightness(20)
    pixel_ring.change_pattern('echo')
    
    #Possible inputs and choices
    if n == 0:
        print "Choice 1"
        wakeup()
    elif n == 1:
        print "Choice 2"
        think()
    elif n == 2:
        print "Choice 3"
        listen()
    elif n == 3:
        print "Choice 4"
        print inspect.getmodule(pixel_ring)
        speak()
    elif n == 4:
        print "Choice 5"
        trace()

#LED functions
#To write more funtions, go to apa102_pixel_ring.py 
#from the pixel ring folder
def wakeup():
    pixel_ring.wakeup()
    time.sleep(3)
    pixel_ring.think()
    time.sleep(3)
    
    powerOff()

def think():
    pixel_ring.think()
    time.sleep(3)
    
    powerOff()
    
def listen():
    pixel_ring.listen()
    time.sleep(3)
    
    powerOff()
    
def speak():    
    pixel_ring.speak()
    time.sleep(3)
    
    powerOff()
    
def trace():
    pixel_ring.trace()
    time.sleep(3)
    
    powerOff()
    
def powerOff():
    pixel_ring.off()
    power.off()
    time.sleep(1)
    
if __name__ == '__main__':
    
    wakeup()
