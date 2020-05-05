#!/usr/bin/env python3

import subprocess
from gpiozero import MotionSensor
import datetime
import picamera
import time
#import ConfigParser
import configparser
import glob
import os
import pika
import json
import base64
import netifaces

mq_server = "mq_server.yw.com"
mq_server_port = "80"

web_server = "web_server.yw.com"
web_server_port = "80"
#
#message queue, send message to remote server using RabbitMQ
#
def send(document):
	credentials = pika.PlainCredentials(username='test', password='test')
	connection = pika.BlockingConnection(
	pika.ConnectionParameters(host=mq_server, credentials=credentials))

	channel = connection.channel()

	channel.queue_declare(queue= 'queue')

	channel.basic_publish(exchange='', routing_key= 'queue', body= document)
	print(" [x] Sent " + document)
	connection.close()
#
#returns string that contains the first mac address found, if no mac address found returns "none"
#
def findMac():
	interfaces = netifaces.interfaces()
	for n in interfaces:
		address = netifaces.ifaddresses(n)
		mac = address[netifaces.AF_LINK][0]
		mac_address = mac['addr']
		if (mac_address != '00:00:00:00:00:00'):
			return mac_address
	return "none" 
#
#creates motion sensor config file: gets info from web server and updates config file in /etc
#
def get_email_info():
	getInfo = "curl http://" + web_server + ":" + web_server_port + "/EMAIL_INFO.txt -o test.txt" 
	subprocess.call(getInfo, shell = True)
	
	f1 = open('/etc/motion_sensor.conf', 'wb')
	f2 = open('/home/pi/motion_sensor/motion_sensor.conf.noEmail', 'rb')
	f3 = open('/home/pi/motion_sensor/test.txt', 'rb')

	a = f2.read()
	b = f3.read()
#	f1.write("#it works")	
	f1.write(a)	
	f1.write(b)

	f1.close()
	f2.close()
	f3.close()

get_email_info()

motion_sensor_conf = r'/etc/motion_sensor.conf'
config = configparser.RawConfigParser()
config.read(motion_sensor_conf)

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
#
#writes html for image.html and sends it over to the web server
#
def update_webpage(image_name):
	image_location = config.get('settings', 'image_location')
	mac_address = findMac()
	html_code = '<html> <p style = "font-size: 100%">Photo taken on ' + image_name[5:15] +' at ' + image_name[-9:-4] + ' from MAC Address: ' + mac_address + '</p> <img src = image/' + image_name + ' alt = "image" style = "width:500px"></html>'
	f = open(image_location, "w")
	f.write('#image.html\n<html> <p style = "font-size: 100%">Photo taken on ' + image_name[5:15] +' at ' + image_name[-9:-4] + '</p> <img src = image/' + image_name + ' alt = "image" style = "width:500px"></html>')
	f.close()
	# a Python object (dict):
	x = {"name": image_location, "content": html_code, "mac": mac_address}
	# convert into JSON:
	y = json.dumps(x)

	# the result is a JSON string:
	print(y)

	send(y)
#
#writes html for links.html and sends it over to the web server
#
def update_past_images():
	link_location = config.get('settings', 'link_location')
	f = open(config.get('settings', 'link_location'), "w")
	f.write('<html>')
	f.close()
	f = open(config.get('settings', 'link_location'), "a")
	counter = 0
	for image in sorted(glob.glob(config.get('settings', 'location') + '*'), reverse = True):
		f.write('<a href = "' + image[9:] + '">Photo taken on ' + image[20:30] +' at ' + image[-9:-4] + '</a> <p> </p>')
		counter += 1
		if counter == 5:
			break
	f.write('</html>')
	f.close()
	mac_address = findMac()
	f = open(config.get('settings', 'link_location'), "r")
	link_code = f.read()
	print(link_code)
        # a Python object (dict):
	x = {"name": link_location, "content": link_code, "mac": mac_address}
        # convert into JSON:
	y = json.dumps(x)

        # the result is a JSON string:
	print(y)

	send(y)

#takes a picture
def take_picture():
	camera = picamera.PiCamera()
	camera.start_preview()
	time.sleep(2)
	image_name = "image" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M") + '.jpg'
	full_image_name = config.get('settings', 'location') + image_name 
	update_webpage(image_name)
	update_past_images()
	camera.capture(full_image_name)
	camera.stop_preview()
	camera.close()
	f = open(full_image_name, "rb")
	content = f.read()
	f.close()
	mac_address = findMac()
	msg = base64.b64encode(content).decode("utf-8")
        # a Python object (dict):
	x = {"name": full_image_name, "content": msg, "mac": mac_address}
        # convert into JSON:
	y = json.dumps(x)

        # the result is a JSON string:
	print(y)

	send(y)
	return(full_image_name)
