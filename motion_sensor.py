#!/usr/bin/env python3
import time
import sensor
import datetime
import configparser



#reads motion_sensor.conf for image location, pin, email_enabled, and email
motion_sensor_conf = r'/etc/motion_sensor.conf'
config = configparser.RawConfigParser()
config.read(motion_sensor_conf)

mq_server = config.get('settings', 'mq_server')
mq_server_port = config.get('settings', 'mq_server_port') 

web_server = config.get('settings', 'web_server') 
web_server_port = config.get('settings', 'web_server_port') 

mac_address = sensor.findMac()
#updates config file
sensor.get_email_info(web_server)

location = config.get('settings', 'location')
image_location = config.get('settings', 'image_location')
link_location = config.get('settings', 'link_location')
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
		image_name = sensor.take_picture(location)
		full_image_name = location + image_name
		image_json = sensor.picture_to_json(full_image_name)
		sensor.send(image_json, mq_server)
	
		sensor.update_webpage(image_name, image_location, mac_address)
		image_html_json = sensor.convert_to_json(image_location, mac_address)
		sensor.send(image_html_json, mq_server)
	
		sensor.update_past_images(link_location)
		links_html_json = sensor.convert_to_json(link_location, mac_address)
		sensor.send(links_html_json, mq_server)

		sensor.get_email_info(web_server)
		if email_enabled == 'on':
			sensor.send_email(email, subject, message)
			sensor.send_email(image_email, 'Image_of_Motion', message, full_image_name) 
		time.sleep(600)

