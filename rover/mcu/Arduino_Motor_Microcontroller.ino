#include <Servo.h>
Servo myservo1;  //Left wheel
Servo myservo2;  //Right wheel
float pseudoSpeed1 = -1; //forward/backward
float pseudoSpeed2 = -0.8; //right/left
float pseudoSpeed3 = -0.5; //rotate right/left about centre axis

void setup () {
  //PWM control wheels
  myservo1.attach(6);
  myservo2.attach(7);
  Serial.begin(9600);
}

void loop(){
  moveRover();
}

//Takes in a number from -1 to 1 and converts to 31 to 159
int custom_map(float num){
  int adjustedSpeed;
  
  if (num >= 0){
    adjustedSpeed = 69*num+90; 
  }
  else if (num <= 0){
    adjustedSpeed = 59*num+90;
  }
  return adjustedSpeed;
}

void wheel_rotate(Servo servo, float joystickSpeed){
  servo.write(custom_map(joystickSpeed));
}

void moveRover(){
 if (pseudoSpeed2 == 0 && pseudoSpeed3 == 0){  //Move Forward/Backward
   wheel_rotate(myservo1, pseudoSpeed1);
   wheel_rotate(myservo2, pseudoSpeed1);
 }
 else if (pseudoSpeed2 > 0 && pseudoSpeed3 == 0){  //Right Turn
   wheel_rotate(myservo1, pseudoSpeed1);
   wheel_rotate(myservo2, pseudoSpeed1*(1-abs(pseudoSpeed2))); //Right wheel ranges from 0 to pseudoSpeed1 (determines angle of turn)
 }
 else if (pseudoSpeed2 < 0 && pseudoSpeed3 == 0){  //Left Turn
   wheel_rotate(myservo1, pseudoSpeed1*(1-abs(pseudoSpeed2))); //Left wheel ranges from 0 to pseudoSpeed1 (determines angle of turn)
   wheel_rotate(myservo2, pseudoSpeed1);
 }
 else{ // pseudoSpeed3 != 0; Rotate rover about centre axis
   wheel_rotate(myservo1, pseudoSpeed3);
   wheel_rotate(myservo2, -pseudoSpeed3);
 }
}
