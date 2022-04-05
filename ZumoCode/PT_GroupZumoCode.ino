#include <Zumo32U4Motors.h>
#include <Zumo32U4ProximitySensors.h>
#include <Zumo32U4Encoders.h>
#include <Zumo32U4Buzzer.h>

Zumo32U4Motors motors;
Zumo32U4ProximitySensors proxSensors;
Zumo32U4Encoders encoders;
Zumo32U4Buzzer buzzer;

// Speed Declarations
#define BACKWARD_SPEED    500
#define MOVE_SPEED        1000
#define TURN_SPEED        1000
#define HALT              0


int robotStatus;
int incomingByte; // for incoming serial data
int rightSpeed = 0;
int leftSpeed = 0;

void setup() {
  // put your setup code here, to run once:
  // Serial1 takes in the port number 9600 so it can listen for incoming messages
  Serial1.begin(9600);
  incomingByte = Serial1.read();

  proxSensors.initFrontSensor();
  delay(100);
  encoders.init();

  robotStatus = 0;

}

void loop() {
  // put your main code here, to run repeatedly:
  switch (robotStatus) {
    case 0:
      manualControl();
      break;
    }

}

void manualControl() {
    //This will speed down the engine unless a command to speed up is received
  if(abs(rightSpeed)>0){rightSpeed=rightSpeed-rightSpeed/5;}
  if(abs(leftSpeed)>0){leftSpeed=leftSpeed-leftSpeed/5;}
  motors.setRightSpeed(rightSpeed);
  motors.setLeftSpeed(leftSpeed);
  incomingByte = Serial1.read();
  
//  if (Serial1.available() > 0){
    switch(incomingByte){
      case 'a':// turn left
        rightSpeed=rightSpeed+400;
        break;
     case 'd': // turn right
        leftSpeed=leftSpeed+400;
        break;
     case 'w': // forward
        rightSpeed=rightSpeed+400;
        leftSpeed=leftSpeed+400;
        break;
     case 's':// backward
        rightSpeed=rightSpeed-400;
        leftSpeed=leftSpeed-400;
        break;
     case'x':
        rightSpeed = 0;
        leftSpeed = 0; 
        break;
     case 'o':
        robotStatus = 0;
        break;
     case 'v':
        buzzer.playFrequency(500,250,10);
        break;
      }
      
      delay(20);
};
