from gpiozero import MotionSensor
import time
import os
#import scrollphat
from time import gmtime, strftime
import time
import sys
import bisect

pir = MotionSensor(4)
while True:
	if pir.motion_detected:
		print("Motion detected")	


