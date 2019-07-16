#imports from vad doa
import sys
import webrtcvad
import numpy as np
from pixel_ring import pixel_ring
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
	pixelDirection = 0;
		
	#For the direction of arrival
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
			sys.stdout.write('1') #Sound detected
		    else:
			sys.stdout.write('0') #No sound detected

		    sys.stdout.flush()

		    chunks.append(chunk)
		    
		    if len(chunks) == doa_chunks:             
			if speech_count > (doa_chunks / 2):
			    frames = np.concatenate(chunks)
			    direction = mic.get_direction(frames)
					
			    if direction > 0 and direction <= 30:
				pixelDirection = 1
			    elif direction > 30 and direction <= 60:
				pixelDirection = 2
			    elif direction > 60 and direction <= 90:
				pixelDirection = 3
			    elif direction > 90 and direction <= 120:
				pixelDirection = 4
			    elif direction > 120 and direction <= 150:
				pixelDirection = 5
			    elif direction > 150 and direction <= 180:
				pixelDirection = 6
			    elif direction > 180 and direction <= 210:
				pixelDirection = 7
			    elif direction > 210 and direction <= 240:
				pixelDirection = 8
			    elif direction > 240 and direction <= 270:
				pixelDirection = 9
			    elif direction > 270 and direction <= 300:
				pixelDirection = 10
			    elif direction > 300 and direction <= 330:
				pixelDirection = 11
			    elif direction > 330 and direction <= 360:
				pixelDirection = 0
							
			    pixels.wakeup()
			    time.sleep(2)
			    pixels.off()
			    print('\n{}'.format(int(direction)))

			speech_count = 0
			chunks = []
						
			#In a format of RGB for colours
			#max number for data (Colour) is 47
			#i is the number of pixel, going as a clock around the speaker with LED num of 0-11
			for i in range(1): 
				self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]))

			self.dev.show()

	except KeyboardInterrupt:
	    pass
				
	pixel_ring.off()



pixels = Pixels()


if __name__ == '__main__':
    while True:

       try:
            pixels.wakeup()
            time.sleep(3)
            pixels.think()
            time.sleep(3)
            pixels.speak()
            time.sleep(6)
            pixels.off()
            time.sleep(3)
        except KeyboardInterrupt:
            break

    pixels.off()
    time.sleep(1)
