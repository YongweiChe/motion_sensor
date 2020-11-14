# Motion Sensor with Object Detection
An python application running on Raspberry PI that detects motion, captures an image, and then identify interested object based on YOLOv3 Object Detection Algorithm. The final image is sent to a website for viewing.  

## Hardware
- Raspberry Pi 2 Model B Rev 1.1
- HC-SR501 PIR Motion Detector
- 5 Megapixels sensor with OV5647 webcam sensor

## How It Works:
- Detect motion with multiple PIR sensors
- Capture a image when motion is detected
- Image is sent to a message queue for object detection
- The image is processed using the YOLOv3 Object Detection Algorithm
- The image is then sent to a message queue for the website
- A web server pull the image from a message queue and update the website with the image

## Code
- The application is written in Python

## Third party software 
- RabbitMQ - https://www.rabbitmq.com/
- YOLOv3 - https://pjreddie.com/darknet/yolo/

## Configuration
- Copy Motion_sensor.py and sensor.py to /usr/local/sbin.
- Change parameters in /etc/motion_sensor.conf

## Start up motion sensor

- Get the IP address of the message queue server and point `mq_server.yw.com` to the IP address
``` 
192.168.1.3    mq_server.yw.com
```

- Open firewall port on the message queue server
```
iptables -I INPUT 2 -p tcp --dport 5672 -s 192.168.x.x/x -j ACCEPT
```

- Start the app
```
suod ./motion_sensor.py
```

### Start up message queue server
- Start message queue server
```
/etc/init.d/rabbitmq-server
```

- Check Message Queue Server Status
```
/usr/sbin/rabbitmqctl status
```

- Open up firewall
```
iptables -I INPUT 2 -p tcp --dport 5672 -s 192.168.x.x/x -j ACCEPT
```
