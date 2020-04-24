# motion_sensor
This is a motion sensor designed to run on a raspberry pi. It detects motion with a cooldown and sends an email if and when it detects motion. It also has a website component that stores the last five pictures detected by the sensor. 

Motion_sensor.py and sensor.py need to be copied to /usr/local/sbin.
You should put your own information into motion_sensor.conf.example and then copy it to /etc.
