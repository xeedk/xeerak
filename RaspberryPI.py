import RPi.GPIO as GPIO

import sys,time,json,uuid,requests,string,re

import smbus

import cv2

import argparse

from picamera.array import PiRGBArray

from picamera import PiCamera

from PIL import Image

cascPath = '/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml'

faceCascade = cv2.CascadeClassifier(cascPath)

I2C_BUS = 1

I2C_SLAVE = 0x12

SMS_INTERRUPT_PIN = 19

CAMERA_INTERRUPT_PIN = 21

smsMessage =""

smsNumber =""

FLAGS = None
    
camera = PiCamera()

time.sleep(0.1)

camera.resolution = (640, 480)

camera.hflip = True

camera.vflip = True

camera.framerate = 32

rawCapture = PiRGBArray(camera, size=(640, 480))

def detectFace():
    
  for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
      image = frame.array

      frame.truncate(0)

      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      blur=cv2.Laplacian(gray, cv2.CV_64F).var()
      if blur > 20:
          faces = faceCascade.detectMultiScale(
             gray,
             scaleFactor=1.1,
             minNeighbors=5,
             minSize=(30, 30),
             flags=cv2.CASCADE_SCALE_IMAGE
          )
          if(len(faces) > 0):
              fileName= 'face_' + str(str(uuid.uuid4())) + '.jpg'
              print(fileName)
              cv2.imwrite(fileName,image)
              time.sleep(1);
                
              return fileName



def readMessageFromArduino():
    valid_characters = string.printable
    global smsMessage
    c = ""
    while c != 'M':
       data_received_from_Arduino = ""
       smsMessage = ""
       data_received_from_Arduino = i2c.read_i2c_block_data(I2C_SLAVE, 0,30)
       for i in range(len(data_received_from_Arduino)):
         smsMessage += chr(data_received_from_Arduino[i])
       c=smsMessage[0]

    data_received_from_Arduino =""
    tempString = ''.join(i for i in str(smsMessage) if i in valid_characters)
    processSms(tempString)
    smsMessage = ""

def processSms(smsMessage):
   try:
       smsRegex = re.split(';',smsMessage)
       data = {'smsNumber': smsRegex[1], 'smsText' : smsRegex[0]}       
       reqUrl = FLAGS.cs + '/api/smsRecognize/'
       req= requests.post(reqUrl, data=data) 
       res=json.loads(req.text)
       if res['status'] == "Ok":
           i2c.write_byte(I2C_SLAVE,1)
           print("Gate Open Signal Sent to Arduino")
       
   except:
       pass    



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--cs',
      type=str,
      default='http://192.168.1.72:9000',
      help='Centeraliazed Server Address'
     )
    parser.add_argument(
        '--haarcascade',
        type=str,
        default='',
        help='haarcascade file for detecting face'
       )
    FLAGS, unparsed = parser.parse_known_args() 
    
    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(SMS_INTERRUPT_PIN, GPIO.IN)
    GPIO.setup(CAMERA_INTERRUPT_PIN, GPIO.IN)
    i2c = smbus.SMBus(I2C_BUS)

    GPIO.add_event_detect(SMS_INTERRUPT_PIN, GPIO.RISING)
    GPIO.add_event_detect(CAMERA_INTERRUPT_PIN, GPIO.RISING)    
    while 1:
            try:
              if GPIO.event_detected(SMS_INTERRUPT_PIN):
                 print("Sms Received: Readin Now\n")
                 readMessageFromArduino()

    
              if GPIO.event_detected(CAMERA_INTERRUPT_PIN):
                  image = detectFace()                   
                  files = {'image_file': open(image,"rb")}
                  reqUrl = FLAGS.cs + '/api/imageRecognize/'
                  req = requests.post(reqUrl, files=files)
                  res=json.loads(req.text)
                  print(res)
                  if res['status'] == "Ok":
                      i2c.write_byte(I2C_SLAVE,1)
                      print("Gate Open Signal Sent to Arduino")
                  else:
                      i2c.write_byte(I2C_SLAVE,2)
                      print("Bell Ring Signal Sent to Arduino")
        
            except:
                 pass
