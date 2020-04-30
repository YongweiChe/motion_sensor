#!/usr/bin/env python3

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

