#!/usr/bin/python

import subprocess
from gpiozero import MotionSensor
import datetime
import picamera
import time
import ConfigParser
import glob

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

def update_webpage(image_name):
                f = open("/var/www/image.html", "w")
                f.write('<html> <p style = "font-size: 100%">Photo taken on ' + image_name[5:15] +' at ' + image_name[-9:-4] + '</p> <img src = image/' + image_name + ' alt = "image" style = "width:500px"></html>')
                f.close()

def update_past_images():
	f = open("/var/www/links.html", "w")
	f.write('<html>')
	f.close()
	f = open("/var/www/links.html", "a")
	for image in glob.glob('/var/www/image/*'):
		f.write('<a href = "' + image[9:] + '">Photo taken on ' + image[20:30] +' at ' + image[-9:-4] + '</a> <p> </p>')
	f.write('</html>')
	f.close()

#takes a picture
def take_picture():
	config = ConfigParser.RawConfigParser()
	conf = r'settings.conf'
	config.read(conf)

        camera = picamera.PiCamera()
        camera.start_preview()
        time.sleep(2)
	image_name = "image" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M") + '.jpg'
	full_image_name = config.get('settings', 'location') + image_name 
	update_webpage(image_name)
	camera.capture(full_image_name)
        camera.stop_preview()
	camera.close()
	return(full_image_name)
