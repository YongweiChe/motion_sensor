#!/usr/bin/python

import subprocess
from gpiozero import MotionSensor

def detect_motion(pin):
	pir = []
	for n in pin:
		pir.append(MotionSensor(n))
	
	for n in pir:
		if(n.motion_detected is True):
			return True
	return False

def send_email(email, subject, message):
        send = 'echo ' +  message + ' | mutt -s ' + subject + ' -- ' + email
        subprocess.call(send, shell=True)

