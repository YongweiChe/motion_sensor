#!/usr/bin/python2
import os
import sensor
import sys
import time

pin = [17, 4, 11, 18]
email_enabled = True
email = "hjhuwei1@gmail.com"

while True:
	if sensor.detect_motion(pin) is True:
		if email_enabled is True:
			sensor.send_email(email, "test", "test")
		time.sleep(3600)


