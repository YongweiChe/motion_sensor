#!/usr/bin/env python3
import pika
import json
import base64
import netifaces

def findMac():
	interfaces = netifaces.interfaces()
	for n in interfaces:
		address = netifaces.ifaddresses(n)
		mac = address[netifaces.AF_LINK][0]
		mac_address = mac['addr']
		if (mac_address != '00:00:00:00:00:00'):
			return mac_address
	return "none" 
	   
mac_address = "b8:27:eb:43:b5:2c"
print(mac_address)
credentials = pika.PlainCredentials(username='test', password='test')
connection = pika.BlockingConnection(
	pika.ConnectionParameters(host='mq_server.yw.com', credentials=credentials))
channel = connection.channel()


channel.queue_declare(queue=mac_address)

def callback(ch, method, properties, body):
	body = body.decode()	
	y = json.loads(body)

	content = y["content"]
	if(y["name"].find('.jpg') != -1):
		print("in here1")
		content = base64.b64decode(content)

	f = open(y["name"], "w")
	f.write(content)
	f.close()
	print("Received %r" % method.routing_key)

channel.basic_consume(
	queue=mac_address, on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

