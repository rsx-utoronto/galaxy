//Range of rotate() function: 31-159
#include <Servo.h>
Servo myservo1;
Servo myservo2;
float pseudoSpeed1 = -1; //forward+backward
float pseudoSpeed2 = -0.8; //right+left
float pseudoSpeed3 = -0.5; //rotate right and left

void setup () {
  myservo1.attach(6); // Use PWM pin 14 to control Sabertooth.
  myservo2.attach(7);
  Serial.begin(9600);
}

void loop(){
  moveRover();
}

//Takes in a number from -1 to 1 and converts to 31 to 159
int custom_map(float num){
  int adjustedSpeed;
  
  if (num>=0){
    adjustedSpeed = 69*num+90; 
  }
  else if (num<=0){
    adjustedSpeed = 59*num+90;
  }
  return adjustedSpeed;
}

void wheel_rotate(Servo servo, float joystickSpeed){
  servo.write(custom_map(joystickSpeed));
}

void moveRover(){
 if (pseudoSpeed2 == 0 && pseudoSpeed3 == 0){
   wheel_rotate(myservo1, pseudoSpeed1);
   wheel_rotate(myservo2, pseudoSpeed1);
 }
 else if (pseudoSpeed2 > 0 && pseudoSpeed3 == 0){
   wheel_rotate(myservo1, pseudoSpeed1);
   wheel_rotate(myservo2, pseudoSpeed1*(1-abs(pseudoSpeed2)));   
 }
 else if (pseudoSpeed2 < 0 && pseudoSpeed3 == 0){
   wheel_rotate(myservo1, pseudoSpeed1*(1-abs(pseudoSpeed2)));
   wheel_rotate(myservo2, pseudoSpeed1);
 }
 else if(pseudoSpeed3 != 0){
   wheel_rotate(myservo1, pseudoSpeed3);
   wheel_rotate(myservo2, -pseudoSpeed3);
 }
}
