#!/usr/bin/python

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

def send(document):
	credentials = pika.PlainCredentials(username='test', password='test')
	connection = pika.BlockingConnection(
	pika.ConnectionParameters(host='192.168.1.10', credentials=credentials))

	channel = connection.channel()

	channel.queue_declare(queue='hello')

	file = open(document, "rb")
	image = file.read()
	file.close()

	channel.basic_publish(exchange='', routing_key='hello', body= image)
	print(" [x] Sent " + document)
	connection.close()

def get_email_info():
	getInfo = "curl http://192.168.1.10:80/EMAIL_INFO.txt -o test.txt" 
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

def update_webpage(image_name):
	image_location = config.get('settings', 'image_location')
	f = open(image_location, "w")
	f.write('<html> <p style = "font-size: 100%">Photo taken on ' + image_name[5:15] +' at ' + image_name[-9:-4] + '</p> <img src = image/' + image_name + ' alt = "image" style = "width:500px"></html>')
	f.close()
	#send(image_location)
	upload = "curl -X POST -H 'Content-Type: multipart/form-data' -F 'my_image=@" + image_location + "' http://192.168.1.10:8080/uploader"
	print(upload)
	subprocess.call(upload, shell = True) 


def update_past_images():
	print("in update_past_images")
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
	upload = "curl -X POST -H 'Content-Type: multipart/form-data' -F 'my_image=@" + link_location + "' http://192.168.1.10:8080/uploader"
	print(upload)
	subprocess.call(upload, shell = True)

#takes a picture
def take_picture():
	camera = picamera.PiCamera()
	camera.start_preview()
	time.sleep(2)
	image_name = "image" + datetime.datetime.now().strftime("%Y-%m-%d_%H:%M") + '.jpg'
	full_image_name = config.get('settings', 'location') + image_name 
	update_webpage(image_name)
	print("before\n\n\n\n")
	update_past_images()
	print("after\n\n\n\n\n")
	camera.capture(full_image_name)
	camera.stop_preview()
	camera.close()
	upload = "curl -X POST -H 'Content-Type: multipart/form-data' -F 'my_image=@" + full_image_name + "' http://192.168.1.10:8080/uploader" 
	print(upload)
	subprocess.call(upload, shell = True)	
	return(full_image_name)
