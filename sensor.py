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

######
# parameterize 
# - routing_key = "queue"
# - username = "test"
# - password = "test"
######
#
# message queue, send message to remote server using RabbitMQ
#
def send(json_document, mq_server, mq_server_port="5672", username="test", password="test", routing_key="queue"):
	credentials = pika.PlainCredentials(username=username, password=password)
	connection = pika.BlockingConnection(
	pika.ConnectionParameters(host=mq_server, port=mq_server_port, credentials=credentials))

	channel = connection.channel()

	channel.queue_declare(queue=routing_key)

	channel.basic_publish(exchange='', routing_key=routing_key, body=json_document)
	print(" [x] Sent ")
	connection.close()
#
# returns string that contains the first mac address found, if no mac address found returns "none"
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
# writes html for image.html and sends it over to the web server
#
def update_webpage(image_name, image_location, mac_address):
	html_code = '<html> <p style = "font-size: 100%">Photo taken on ' + image_name[5:15] +' at ' + image_name[-9:-4] + ' from MAC Address: ' + mac_address + '</p> <img src = image/' + image_name + ' alt = "image" style = "width:500px"></html>'
	f = open(image_location, "w")
	f.write('#image.html\n<html> <p style = "font-size: 100%">Photo taken on ' + image_name[5:15] +' at ' + image_name[-9:-4] + '</p> <img src = image/' + image_name + ' alt = "image" style = "width:500px"></html>')
	f.close()
	
#
# writes html for links.html and sends it over to the web server
#
def update_past_images(link_location):
	f = open(link_location, "w")
	f.write('<html>')
	f.close()
	f = open(link_location, "a")
	counter = 0
	for image in sorted(glob.glob(link_location + '*'), reverse = True):
		f.write('<a href = "' + image[9:] + '">Photo taken on ' + image[20:30] +' at ' + image[-9:-4] + '</a> <p> </p>')
		counter += 1
		if counter == 5:
			break
	f.write('</html>')
	f.close()

def convert_to_json(html_location, mac_address):
	f = open(html_location, "r")
	html_code = f.read()
	print(html_code)
	# a Python object (dict):
	x = {"name": html_location, "content": html_code, "mac": mac_address}
	# convert into JSON:
	y = json.dumps(x)

	# the result is a JSON string:
	return y

def take_picture(location):
	camera = picamera.PiCamera()
	camera.start_preview()
	time.sleep(2)
	image_name = "image" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M") + '.jpg'
	full_image_name = location + image_name
	camera.capture(full_image_name)
	camera.stop_preview()
	camera.close()
	return(image_name)

def picture_to_json(location, image_name):
	full_image_name = location + image_name
	f = open(full_image_name, "rb")
	content = f.read()
	f.close()
	mac_address = findMac()
	msg = base64.b64encode(content).decode("utf-8")
	# a Python object (dict):
	x = {"name": image_name, "content": msg, "mac": mac_address}
	# convert into JSON:
	y = json.dumps(x)

	# the result is a JSON string:
	return y

