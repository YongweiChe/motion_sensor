#!/usr/bin/python

import time
from gpiozero import MotionSensor

def check_motion(pin):
	pir = []
	for n in pin:
		pir.append(MotionSensor(n))
	
	for n in pir:
		if(n.motion_detected is True):
			return True
	return False

