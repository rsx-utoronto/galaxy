//range: 31-159
#include <Servo.h>
Servo myservo1;
Servo myservo2;

int joystickSpeed = 0;//serial.read (whatever come from the joystick speed)
float pseudoSpeed = 0; 

void setup () {
  myservo1.attach(6); // Use PWM pin 14 to control Sabertooth.
  myservo2.attach(7);
  Serial.begin(9600);
}

void loop(){
  sortSpeed(pseudoSpeed);
}

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

void sortSpeed(float joystickSpeed){
  forward(custom_map(joystickSpeed)); 
}

void forward(int speed1){
  myservo1.write(speed1);
}
