#imports from vad doa
import sys
import webrtcvad
import numpy as np
from mic_array import MicArray

import apa102
import time
import threading
from gpiozero import LED
try:
    import queue as Queue
except ImportError:
    import Queue as Queue

from alexa_led_pattern import AlexaLedPattern
from google_home_led_pattern import GoogleHomeLedPattern

RATE = 16000
CHANNELS = 4
VAD_FRAMES = 10     # ms
DOA_FRAMES = 200    # ms

direction = 0
ledDirection = 0

#from pixels.py
class Pixels:
    PIXELS_N = 12

    def __init__(self, pattern=AlexaLedPattern):
        self.pattern = pattern(show=self.show)

        self.dev = apa102.APA102(num_led=self.PIXELS_N)
        
        self.power = LED(5)
        self.power.on()

        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

        self.last_direction = None

    def wakeup(self, direction=0):
        self.last_direction = direction
        def f():
            self.pattern.wakeup(direction)

        self.put(f)

    def listen(self):
        if self.last_direction:
            def f():
                self.pattern.wakeup(self.last_direction)
            self.put(f)
        else:
            self.put(self.pattern.listen)

    def think(self):
        self.put(self.pattern.think)

    def speak(self):
        self.put(self.pattern.speak)

    def off(self):
        self.put(self.pattern.off)

    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    def show(self, data):
	#For the wanted LED, it has to be 1 less of ledDirection as for loop starts at 0
	for i in range(ledDirection):
	    #get direction of sound, pair with LED and show
	    if i == ledDirection - 1:
		# Activate led and its RGB property
		# Have three, one before and after where the direction is coming from to make the lights more noticable
		#You can change the colour of LED through the format of int(data[4*i + 1]) by having i with different numbers
		if ledDirection == 1: 	#If the direction is at the first LED, light up the one before it
		    self.dev.set_pixel(12 - 1, int(data[4*2 + 1]), int(data[4*2 + 2]), int(data[4*2 + 3])) 	#before middle led
		else: 	#act normally
		    self.dev.set_pixel(i - 1, int(data[4*2 + 1]), int(data[4*2 + 2]), int(data[4*2 + 3]))
		self.dev.set_pixel(i, int(data[4*2 + 1]), int(data[4*2 + 2]), int(data[4*2 + 3]))	#middle led
		self.dev.set_pixel(i + 1, int(data[4*2 + 1]), int(data[4*2 + 2]), int(data[4*2 + 3]))	#after middle led
		break
	    #if main LED direction is the last one, light up the one after and before the LED
	    elif ledDirection == 12:
		self.dev.set_pixel(0, int(data[4*2 + 1]), int(data[4*2 + 2]), int(data[4*2 + 3]))
		self.dev.set_pixel(11, int(data[4*2 + 1]), int(data[4*2 + 2]), int(data[4*2 + 3]))
		self.dev.set_pixel(10, int(data[4*2 + 1]), int(data[4*2 + 2]), int(data[4*2 + 3]))
		
        self.dev.show()


pixels = Pixels()

def getDirection():
    #From vad_doa
    vad = webrtcvad.Vad(3)

    speech_count = 0
    chunks = []
    doa_chunks = int(DOA_FRAMES / VAD_FRAMES)

    try:
        with MicArray(RATE, CHANNELS, RATE * VAD_FRAMES / 1000)  as mic:
            for chunk in mic.read_chunks():
                # Use single channel audio to detect voice activity
                if vad.is_speech(chunk[0::CHANNELS].tobytes(), RATE):
                    speech_count += 1

                sys.stdout.flush()

                chunks.append(chunk)
		# If sound is picked up, get direction of sound through estimation algorithm
                if len(chunks) == doa_chunks:                 
                    if speech_count > (doa_chunks / 2):
                        frames = np.concatenate(chunks)
			#get direction
                        direction = mic.get_direction(frames)
                        print('\n{}'.format(int(direction)))
			# I used this to break from the loop once sound and direction is detected
			if direction > 0:
			    return direction
			    break
                    speech_count = 0
                    chunks = []

    except KeyboardInterrupt:
        pass
        
if __name__ == '__main__':
    direction = getDirection()
    
    # The direction of which LED is calculated, depending on which angle it can from
    # It will use which LED is chosen
    # It also only loops once for now
    if direction > 0 and direction <= 30:
	ledDirection = 1
    elif direction > 30 and direction <= 60:
	ledDirection = 2
    elif direction > 60 and direction <= 90:
	ledDirection = 3
    elif direction > 90 and direction <= 120:
	ledDirection = 4
    elif direction > 120 and direction <= 150:
	ledDirection = 5
    elif direction > 150 and direction <= 180:
	ledDirection = 6
    elif direction > 180 and direction <= 210:
	ledDirection = 7
    elif direction > 210 and direction <= 240:
	ledDirection = 8
    elif direction > 240 and direction <= 270:
	ledDirection = 9
    elif direction > 270 and direction <= 300:
	ledDirection = 10
    elif direction > 300 and direction <= 330:
	ledDirection = 11
    elif direction > 330 and direction <= 360:
	ledDirection = 12

    pixels.wakeup()
    time.sleep(3)

    pixels.off()
    time.sleep(1)
