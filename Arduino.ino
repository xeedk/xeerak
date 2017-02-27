
#include <GSM.h>
#include <Wire.h>
#include <Arduino.h>

#include "DISTModule.h"



#define ARDUINO_SLAVE_ADDRESS 0x12


// Gsm Module Declarations

GSM gsmAccess;

GSM_SMS sms;

// Ultrasonic Sensor
DISTModule distanceSensor = DISTModule();

//this will be used to store the incoming message sender number

char senderNumber[20];

//this will be used to store the incoming message (M is used as a flag for PI: That message)

String message = String("M");

int dataReceivedFromPI = 0;

//Gate is connected to Pin 13

const uint8_t gatePin = 13;

//door Bell is connected to pin 12

const uint8_t bellPin = 12;


// Pin 5 is used as an interrupt pin to indicate that a message is onboard

static const char messageInterrupt = 5;

// Pin 5 is used as an interrupt pin to indicate that an object is detected

static const char cameraInterrupt = 4;



void setup() {
  
  Wire.begin(ARDUINO_SLAVE_ADDRESS);
  
  Wire.onReceive(receiveData);
  
  Wire.onRequest(sendData);
  
  Serial.begin(9600);
  
  pinMode(gatePin, OUTPUT);
  
  pinMode(bellPin, OUTPUT);
  
  pinMode(cameraInterrupt, OUTPUT);
  
  pinMode(messageInterrupt, OUTPUT);

  boolean notConnected = true;

  // Start GSM connection

  while (notConnected) {
    
    if (gsmAccess.begin() == GSM_READY) {
      
      notConnected = false;
      
    } else {
      
      Serial.println("Not connected");
      
      delay(1000);
    }
    
  }

  Serial.println("System Initialized ");
  
}

void loop() {
  
  char c;
  
  if (sms.available()) 
  {
    Serial.println("Message received from:");

    sms.remoteNumber(senderNumber, 20);
    
    Serial.println(senderNumber);

    // Read message bytes and print them
    while (c = sms.read()) {
        message += String(c);     
        }

    Serial.println(message);

    message += ';';
    
    message += String(senderNumber);
    
    
    trigger_messageInterrupt();
    
    delay(100);
    
    message = "M";
    
    sms.flush();
    
    Serial.println("MESSAGE DELETED");
    
  }

  if(distanceSensor.detectObject()) 
  {
      
        trigger_CameraInterrupt();

  }    

}



void trigger_messageInterrupt() {
  
    digitalWrite(messageInterrupt, HIGH);
    
    delay(100);

    digitalWrite(messageInterrupt, LOW);
}



void trigger_CameraInterrupt() {
  
    digitalWrite(cameraInterrupt, HIGH);
    
    delay(100);

    digitalWrite(cameraInterrupt, LOW);
}



void receiveData(int byteCount) {
  
    while(Wire.available()) 
    {
        dataReceivedFromPI = Wire.read();
        
        if(dataReceivedFromPI == 1)
        {
             Serial.println("Opening Thr Gate");
             
             digitalWrite(gatePin,HIGH);
             
             delay(2000);
             
             digitalWrite(gatePin,LOW);

             dataReceivedFromPI = 0;
             
        }
        
        if(dataReceivedFromPI == 2)
        {
             Serial.println("Ringing The Bell");
             
             digitalWrite(bellPin,HIGH);
             
             delay(2000);
             
             digitalWrite(bellPin,LOW);
             
             dataReceivedFromPI = 0;

        }                

    }
}

void sendData(){
  
        Wire.write(message.c_str());   
}
