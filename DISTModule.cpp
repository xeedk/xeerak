#include <Arduino.h>
#include <NewPing.h>
#include "DISTModule.h"

const uint8_t TRIGGER_PIN   =   10;
const uint8_t  ECHO_PIN     =   6;
const uint8_t  DETECTION_DISTANCE   =   20;

NewPing distance  = NewPing(TRIGGER_PIN,ECHO_PIN,DETECTION_DISTANCE);

DISTModule::DISTModule() {

}


boolean DISTModule::detectObject() {

    if(distance.ping_cm() <= DETECTION_DISTANCE && distance.ping_cm() > 0) {
        return true;
    }
    return false;
}
