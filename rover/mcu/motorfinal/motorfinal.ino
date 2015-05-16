#include <Servo.h>

float newData[200]; //We will know the size of the float array

int start = 0; //start keeps track of next float in string to be parsed
int data_index = 0; //data_index keeps track of which index to place float in float array

float verticalSpeed = 0; //forward/backward, joystick element 1
float horizontalSpeed = 0; //right/left; joystick element 0
float rotationSpeed = 0; //rotate right/left about centre axis; joystick element 3

float armspeed = 1;
float clawspeed = 1;
float sidespeed = 1;

float dampingFactor = 0;
Servo myservo1;  //Left wheel
Servo myservo2;  //Right wheel
Servo myservo3; //claw
Servo myservo4; //arm
Servo myservo5; //slider
Servo myservo6; //claw
Servo myservo7; //slider
Servo myservo8; //slider

void setup(){
  //PWM control wheels
  myservo1.attach(6);
  myservo2.attach(7);
  myservo3.attach(8);
  myservo4.attach(9);
  myservo5.attach(10);
  myservo6.attach(11);
  myservo6.attach(12);
  myservo6.attach(13);
  Serial.begin(9600);
  Serial2.begin(9600);
  delay(500);
}

void loop(){
  //Process string and build float array
  if(Serial2.available() > 0){
    data_index = 0;
    start = 0;
    String string = Serial2.readStringUntil('\n');
    //String string = "0.5,1.0,0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0"; //Test String
    
    Serial.println(string);

    for(int i = 0; i < string.length(); i++){
      if(string.substring(i, i+1) == "," || i == string.length()-1){
        if (string.substring(i, i+1) == ","){ //Check for comma to denote end of float in string
          newData[data_index] = string.substring(start, i).toFloat();
        }
        else{ //Account for last float in string
          newData[data_index] = string.substring(start, string.length()).toFloat();
        }
        start = i+1;
        data_index++;
      }
    }
    
  horizontalSpeed = newData[0];
  verticalSpeed = newData[1];
  rotationSpeed = newData[2];
  dampingFactor = (newData[3]+1)/2; //Takes a number from -1 to 1 and converts it to 0 to 1 to control speed range 
  
  Serial.print("Vertical Speed: ");
  Serial.println(verticalSpeed);
  Serial.print("Horizontal Speed: ");
  Serial.println(horizontalSpeed);
  Serial.print("Rotation Speed: ");
  Serial.println(rotationSpeed);
  }
  moveRover(verticalSpeed, horizontalSpeed, rotationSpeed);
  moveArm();
}

//Takes number in range [-1:1] and converts to dampingFactor*[31:59]
int custom_map(float num){
  int adjustedSpeed;
  
  if (num >= 0){
    adjustedSpeed = 69*num*dampingFactor+90; 
  }
  else if (num <= 0){
    adjustedSpeed = 59*num*dampingFactor+90;
  }
  return adjustedSpeed;
}

void actuate_motor(Servo servo, float joystickSpeed){
  servo.write(custom_map(joystickSpeed));
}

void moveRover(float verticalSpeed, float horizontalSpeed, float rotationSpeed){
  float turningSpeed = diagonalSpeed(verticalSpeed, horizontalSpeed);
  
  if(horizontalSpeed != 0 || verticalSpeed != 0){  //Continuous forward/backward/turning movement
    if (horizontalSpeed > 0){  //first and fourth quadrant
      actuate_motor(myservo2, turningSpeed); //left wheel moves faster
      actuate_motor(myservo1, turningSpeed*(1-abs(horizontalSpeed))); //right wheel moves slower wrt left wheel
    }
    else{  //second and third quadrant
      actuate_motor(myservo2, turningSpeed*(1-abs(horizontalSpeed))); //Left wheel moves slower wrt right wheel
      actuate_motor(myservo1, turningSpeed); //Right wheel moves faster
    }
  }
  else{  //Rotate rover about centre axis; only rotate on the spot if the joystick doesn't go forward or backward
    actuate_motor(myservo1, rotationSpeed);
    actuate_motor(myservo2, -rotationSpeed);
  }
}

void moveArm(){
  if (newData[10]){//move claw down
    actuate_motor(myservo3, -1);
  }
  else if (newData[11]){//move claw up
    actuate_motor(myservo3, 1);
  }
  if (newData[12]){//move arm down
    actuate_motor(myservo4, -1);
  }
  else if (newData[13]){//move arm up
    actuate_motor(myservo4, 1);
  }   
  if (newData[14]){//move slider right
    actuate_motor(myservo5, -1);
  }
  else if (newData[15]){//move slider left
    actuate_motor(myservo5, 1);
  }  
}

void moveClaw(){
  if (newData[4]){//close claw
    actuate_servo(myservo6, -1);
  }
  else if (!newData[5]){//open claw
    actuate_servo(myservo6, 1);
  }
  if (newData[6]){//close claw
    actuate_servo(myservo7, -1);
  }
  else if (!newData[8]){//open claw
    actuate_servo(myservo7, 1);
  }
  if (newData[7]){//close claw
    actuate_servo(myservo8, -1);
  }
  else if (!newData[9]){//open claw
    actuate_servo(myservo8, 1);
  }
}

void actuate_servo(Servo servo, int servoSpeed){
  int servoAngle = servo.read();
  if (servoAngle<=180 && servoAngle >=0){
    servoAngle = servoAngle + servoSpeed; 
  }
}

float diagonalSpeed(float vy, float vx){
  float vz = sqrt(vx*vx+vy*vy);
  
  return vz*vy/abs(vy)/sqrt(2);  //Normalize speed for range [-1:1] and direction of vy
}
