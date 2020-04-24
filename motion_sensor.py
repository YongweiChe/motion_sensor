#!/usr/bin/python2
import time
import sensor
import datetime
import ConfigParser

#reads motion_sensor.conf for image location, pin, email_enabled, and email
config = ConfigParser.RawConfigParser()
motion_sensor_conf = sensor.motion_sensor_conf 
config.read(motion_sensor_conf)

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
		sensor.update_past_images()
		if email_enabled == 'true':
			sensor.send_email(email, subject, message)
			sensor.send_email(image_email, 'Image_of_Motion', message, image_name) 
		time.sleep(600)

