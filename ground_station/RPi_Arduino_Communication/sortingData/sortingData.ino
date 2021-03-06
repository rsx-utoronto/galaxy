#include <Servo.h>

float newData[200]; //We will know the size of the float array

int start = 0; //start keeps track of next float in string to be parsed
int data_index = 0; //data_index keeps track of which index to place float in float array

void setup(){
  Servo myservo1;  //Left wheel
  Servo myservo2;  //Right wheel
  float verticalSpeed = -1; //forward/backward, joystick element 1
  float horizontalSpeed = -0.8; //right/left; joystick element 0
  float rotationSpeed = -0.5; //rotate right/left about centre axis; joystick element 3
  
  //PWM control wheels
  myservo1.attach(6);
  myservo2.attach(7);
  
  Serial.begin(9600);
  Serial2.begin(9600);
  delay(500);
  
  
}

void loop(){
  //Process string and build float array
  if(Serial2.available() > 0){

    String string = Serial2.readStringUntil('\n');
    Serial.println(string);

    for(int i = 0; i < string.length(); i++){
      if(string.substring(i, i+1) == "," || i == string.length()-1){
        if (string.substring(i, i+1) == ","){ //Check for comma to denote end of float in string
          newData[data_index] = string.substring(start, string.length()).toFloat();
        }
        else{ //Account for last float in string
          newData[data_index] = string.substring(start, string.length()).toFloat();
        }
        start = i+1;
        data_index++;
      }
    }

    //Print parsed example float array
    for(int i = 0; i < 8; i++){
      Serial.print(newData[i]);
      Serial.print(" ");
    }

    //Serial.flush();
  }
  
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
 if (horizontalSpeed == 0 && rotationSpeed == 0){  //Move Forward/Backward
   wheel_rotate(myservo1, verticalSpeed);
   wheel_rotate(myservo2, verticalSpeed);
 }
 else if (horizontalSpeed > 0 && rotationSpeed == 0){  //Right Turn
   wheel_rotate(myservo1, verticalSpeed);
   wheel_rotate(myservo2, verticalSpeed*(1-abs(horizontalSpeed))); //Right wheel ranges from 0 to verticalSpeed (determines angle of turn)
 }
 else if (horizontalSpeed < 0 && rotationSpeed == 0){  //Left Turn
   wheel_rotate(myservo1, verticalSpeed*(1-abs(horizontalSpeed))); //Left wheel ranges from 0 to verticalSpeed (determines angle of turn)
   wheel_rotate(myservo2, verticalSpeed);
 }
 else{ // rotationSpeed != 0; Rotate rover about centre axis
   wheel_rotate(myservo1, rotationSpeed);
   wheel_rotate(myservo2, -rotationSpeed);
 }
}
