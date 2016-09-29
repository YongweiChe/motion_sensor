#!/usr/bin/python

import time
from gpiozero import MotionSensor
pin = [17, 4, 11, 18]
pir = []
for n in pin:
	pir.append(MotionSensor(n))

while True:
	m = 0
	for n in pir:
		if(n.motion_detected is True):
			print("motion detected at", m)
		if(n.motion_detected is False):
			print("no motion at", m)
		m += 1
	time.sleep(1)

