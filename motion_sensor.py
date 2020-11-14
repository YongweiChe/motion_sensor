#!/usr/bin/env python3
import time
import sensor
import datetime
import configparser
import subprocess
import picamera
import base64
import json


#reads motion_sensor.conf for image location, pin, email_enabled, and email
motion_sensor_conf = r'/etc/motion_sensor.conf'
config = configparser.RawConfigParser()

config.read(motion_sensor_conf)

mq_server = config.get('settings', 'mq_server')
mq_server_port = config.get('settings', 'mq_server_port') 

mq_username = config.get('settings', 'mq_username')
mq_password = config.get('settings', 'mq_password')
routing_key = config.get('settings', 'routing_key')

detection_username = config.get('settings', 'detection_username')
detection_password = config.get('settings', 'detection_password')
detection_key = config.get('settings', 'detection_key')

location = config.get('settings', 'location')
image_location = config.get('settings', 'image_location')

pins_string = config.get('settings', 'pin').split(', ')
pins = []
for number in pins_string:
	number =int(number)
	pins.append(number)

### 
serial   = 's001'
mac_address = sensor.findMac().replace(':','')
image_to_cloud = config.get('settings', 'image_to_cloud').strip(' ').lower()
###
camera = picamera.PiCamera()
camera.start_preview()
max_img_number = 3
i = 0
image_name_prefix = "img_" + serial + "_" + mac_address + "_"

print("image to cloud : %s" % image_to_cloud)

while True:
  i += 1 if (i != max_img_number) else 0
  image_name = image_name_prefix + str(i) + ".jpg"

  camera.capture(image_name)
	
  if image_to_cloud == 'on':
    print ("sending image to cloud")

    f = open(image_name, "rb")
    content = f.read()
    f.close()
    msg = base64.b64encode(content).decode("utf-8")

    x = {"name": image_name, "content": msg, "mac": mac_address}
    y = json.dumps(x)

    sensor.send(y, mq_server, username=detection_username, password=detection_password, routing_key=detection_key)

  time.sleep(3)

camera.stop_preview()
camera.close()
