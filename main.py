#!/usr/bin/python2
import time
import sensor
import datetime
import ConfigParser

#reads settings.conf for image location, pin, email_enabled, and email
config = ConfigParser.RawConfigParser()
conf = r'settings.conf'
config.read(conf)

pins_string = config.get('settings', 'pin').split(', ')
pins = []
for number in pins_string:
	number =int(number)
	pins.append(number)

email_enabled = config.get('settings', 'email_enabled')
email_enabled = email_enabled.strip(' ')
email_enabled = email_enabled.lower()
email = config.get('settings', 'email')
image_email = config.get('settings', 'image_email')
subject = "ALERT_MOTION_DETECTED"
message = "Motion detected on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

#detects motion, if motion is detected, sleep for one hour
while True:
	if sensor.detect_motion(pins) is True:
		image_name = sensor.take_picture()
		if email_enabled == 'true':
			sensor.send_email(email, subject, message)
			sensor.send_email(image_email, 'Image_of_Motion', message, image_name) 
		time.sleep(3600)

