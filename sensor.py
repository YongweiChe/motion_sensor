#!/usr/bin/python

import subprocess
from gpiozero import MotionSensor
import datetime
import picamera
import time
import ConfigParser

def detect_motion(pin):
	pir = []
	for n in pin:
		pir.append(MotionSensor(n))
	
	for n in pir:
		if(n.motion_detected is True):
			return True
	return False

def send_email(email, subject, message, attachment = ''):
	if attachment == '':
        	send = 'echo ' + message + ' | mutt -s ' + subject + ' -- ' + email
	else:
		send = 'echo ' + message + ' | mutt -s ' + subject + ' -a ' + attachment + ' -- ' + email
        subprocess.call(send, shell=True)

#takes a picture
def take_picture():
	config = ConfigParser.RawConfigParser()
	conf = r'settings.conf'
	config.read(conf)

        camera = picamera.PiCamera()
        camera.start_preview()
        time.sleep(2)
	
	image_name = config.get('settings', 'location') + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + '.jpg'
	camera.capture(image_name)
        camera.stop_preview()
	camera.close()
	return(image_name)
