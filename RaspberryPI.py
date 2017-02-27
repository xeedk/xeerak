import RPi.GPIO as GPIO

import sys,time,json,uuid,requests,string,re
import smbus

import cv2


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
#          print("Soooo")
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
       if c == '7':
          print(data_received_from_Arduino)
    #print(str(smsMessage.encode('utf-8')).encode('ascii', errors='ignore'))
    data_received_from_Arduino =""
    tempString = ''.join(i for i in str(smsMessage) if i in valid_characters)
    processSms(tempString)
    smsMessage = ""
    print(tempString)

def processSms(smsMessage):
   try:
       smsRegex = re.split(';',smsMessage)
       data = {'smsNumber': smsRegex[1], 'smsText' : smsRegex[0]}       
       req= requests.post('http://192.168.1.5:9000/api/smsRecognize/', data=data) 
       res=json.loads(req.text)
       if res['status'] == "Ok":
           bus.write_byte(arduinoAddress,9)
           print("Gate Open Signal Sent to Arduino")
           #Here We can annouce the name using the speake and tts. try.
           #the name will come from server
       
   except:

       pass    



camera = PiCamera()
time.sleep(0.1)
camera.resolution = (640, 480)
camera.hflip = True
camera.vflip = True
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))


if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)
    
    GPIO.setup(SMS_INTERRUPT_PIN, GPIO.IN)
    GPIO.setup(CAMERA_INTERRUPT_PIN, GPIO.IN)
    i2c = smbus.SMBus(I2C_BUS)

#    theCam = smartCam()

    GPIO.add_event_detect(SMS_INTERRUPT_PIN, GPIO.RISING)
    GPIO.add_event_detect(CAMERA_INTERRUPT_PIN, GPIO.RISING)    
    while 1:
            try:
              if GPIO.event_detected(SMS_INTERRUPT_PIN):
                 print("Trying To Read Sms Message\n")
                 readMessageFromArduino()
                 #time.sleep(10)
       	      #x = i2c.read_byte(I2C_SLAVE)
    
              if GPIO.event_detected(CAMERA_INTERRUPT_PIN):
                  print("Ok")
                  image = detectFace()                   
                  files = {'image_file': open(image,"rb")}
                  req = requests.post('http://192.168.1.5:9000/api/imageRecognize/', files=files)
                  res=json.loads(req.text)
                  print(res)        
            except:
                 pass
        #except KeyboardInterrupt:
         #      GPIO.cleanup()

