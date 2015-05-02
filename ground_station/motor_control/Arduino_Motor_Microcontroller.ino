#include <Servo.h>
Servo myservo1;
Servo myservo2;
int joystickSpeed = 0;//= Serial.read(whatever come from the joystick speed)
//probably need to use split function to split the array

void setup () {
  myservo1.attach(6); // Use PWM pin 14 to control Sabertooth.
  myservo2.attach(7);
  Serial.begin(9600);
}

void loop() {  

}

void sortSpeed(int joystickSpeed){
  int sortedSpeed = 90+joystickSpeed*89;
  forward(sortedSpeed); 
}

void forward(int speed){
  myservo.write(speed);
}
