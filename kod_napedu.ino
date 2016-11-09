#include <AccelStepper.h>
//http://www.airspayce.com/mikem/arduino/AccelStepper/
AccelStepper motor(AccelStepper::HALF4WIRE,1,2,3,4,true);



int keyone = 0;
int keytwo = 0;
int keythree = 0;
float speed1 = -10;
float speed2 = -50;
float speed3 = -150;
float speed4 = -300;
float speed5 = -500;
float speed6 = -700;
float speed7 = -1000;


long position1 = -40
long position2 = -300
long position3 = -900
long position4 = -1500
long position5 = -2000
long position6 = -5000
long position7 = -20000



int pos = 0;
int setter = 0;




void setup() {
  // put your setup code here, to run once:
pinMode(11, OUTPUT);
pinMode(12, OUTPUT);
pinMode(13, OUTPUT);
pinMode(8, INPUT);
pinMode(9, INPUT);
pinMode(10, INPUT);
digitalWrite(11,LOW);
digitalWrite(12,LOW);
digitalWrite(13,LOW);
digitalWrite(8,HIGH);
digitalWrite(9,HIGH);
digitalWrite(10,HIGH);
digitalWrite(1,LOW);
digitalWrite(2,LOW);
digitalWrite(3,LOW);
digitalWrite(4,LOW);
motor.setCurrentPosition(0);
motor.setAcceleration(200);
motor.setMaxSpeed(2050);


}

void loop() {
  keyone = digitalRead(8);   
  keytwo = digitalRead(9);
  keythree = digitalRead(10);

  if (keyone == LOW)
  {
    setter = 1;
    delay(500);
    while (setter == 1)
    {
      digitalWrite(11,HIGH);
      motor.setSpeed(1000);
      motor.runSpeed();
      keyone = digitalRead(8);
      if (keyone == LOW)
      {
        setter = 0;
        delay(200);
      }
      }
  }
  digitalWrite(11,LOW);
  

  if (keytwo == LOW)
  {
    setter = 1;
    delay(500);
    while (setter == 1)
     {
      digitalWrite(12,HIGH);
      keytwo = digitalRead(9);
      motor.setSpeed(-1000);
      motor.runSpeed();
      if (keytwo == LOW)
      {
        setter = 0;
        delay(200);
      }
    }
  
  }
  digitalWrite(12,LOW);

  if (keythree == LOW)
  {
    delay(500);
    setter = 1;
    keythree = digitalRead(10);
    while (setter == 1)
    {
      digitalWrite(12,HIGH);
      digitalWrite(13,HIGH);
      digitalWrite(11,HIGH);
          motor.moveTo(position1);
          motor.setSpeed(speed1);
                    while (motor.distanceToGo() < 0 )
          {
            motor.runSpeed();
            
          }
          motor.moveTo(position2);
          motor.setSpeed(speed2);
                    while (motor.distanceToGo() < 0 )
          {
            motor.runSpeed();
            
          }
          motor.moveTo(position3);
          motor.setSpeed(speed3);
                    while (motor.distanceToGo() < 0 )
          {
            motor.runSpeed();
            
          }
          motor.moveTo(position4);
          motor.setSpeed(speed4);
                    while (motor.distanceToGo() < 0 )
          {
            motor.runSpeed();
            
          }
                    motor.moveTo(position5);
          motor.setSpeed(speed5);
                    while (motor.distanceToGo() < 0 )
          {
            motor.runSpeed();
            
          }
                    motor.moveTo(position6);
          motor.setSpeed(speed6);
                    while (motor.distanceToGo() < 0 )
          {
            motor.runSpeed();
            
          }
                    motor.moveTo(position7);
          motor.setSpeed(speed7);
                    while (motor.distanceToGo() < 0 )
          {
            motor.runSpeed();
            
          }
       
           
          digitalWrite(12,LOW);
          digitalWrite(13,LOW);
          delay(200);
          setter = 0;
    }
  }
delay(100);
}
  

















