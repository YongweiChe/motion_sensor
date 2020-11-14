# Motion Sensor with Object Detection
An python application running on Raspberry PI that detects motion, captures an image, and then identify interested object based on YOLOv3 Object Detection Algorithm. The final image is sent to a website for viewing.  

## Hardware used in this project:
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

## Software:
- The application is written in Python

## Configuration
- Copy Motion_sensor.py and sensor.py to /usr/local/sbin.
- Change parameters in /etc/motion_sensor.conf

