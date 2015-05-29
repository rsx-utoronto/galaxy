#include <Servo.h>
#include <Wire.h> //I2C Arduino Library
#define address 0x1E //0011110b, I2C 7bit address of HMC5883 compass

//2 moisture sensors 
//3 gas sensors (MQ-4 for Methane & Propane & Butane, MQ-7 for Carbon Monoxide, MQ-8 for Hydrogen Gas)

//GAS SENSOR VALUES
const int AOUTpin1 = A0;//the AOUT pin of the CH4 sensor goes into analog pin A0 of the arduino
const int DOUTpin1 = 22;//the DOUT pin of the CH4 sensor goes into digital pin D22 of the arduino
const int AOUTpin2 = A1;//the AOUT pin of the CO sensor goes into analog pin A1 of the arduino
const int DOUTpin2 = 23;//the DOUT pin of the CO sensor goes into digital pin D23 of the arduino
const int AOUTpin3 = A2;//the AOUT pin of the H2 sensor goes into analog pin A2 of the arduino
const int DOUTpin3 = 24;//the DOUT pin of the H2 sensor goes into digital pin D24 of the arduino

float Ro = 10000.0;
float CH4Vrl = 0.0;
float CH4Rs = 0.0;
float CH4ratio = 0.0;
float CH4ppm = 0.0;

float COVrl = 0.0;
float CORs = 0.0;
float COratio = 0.0;
float COppm = 0.0;

float H2Vrl = 0.0;
float H2Rs = 0.0;
float H2ratio = 0.0;
float H2ppm = 0.0;

int CH4limit, COlimit, H2limit;
int CH4Value, COValue, H2Value;

//MOISTURE & RAIN SENSOR
const int moistPin1 = A3;
const int moistPin2 = A4;
int moistValue1 = 0;
int moistValue2 = 0;

float angle; //GPS angle

float newData[200]; //We will know the size of the float array

int start = 0; //start keeping track of next float in string to be parsed
int data_index = 0; //data_index keeps track of which index to place float in float array

float verticalSpeed = 0; //forward/backward, joystick element 1
float horizontalSpeed = 0; //right/left; joystick element 0
float rotationSpeed = 0; //rotate right/left about centre axis; joystick element 3
float dampingFactor = 1; //Damping factor to control speed range
float forw_backFactor = 1; //Dampen either forward or backward wheels to make forward & 
                           //backward motors move at same speed; APPLY TO FASTER MOTOR PAIR

//**********PARAMETERS TO BE SET AT BEGINNING**********
float armSpeed = 1;
float clawSpeed = 1;
float sliderSpeed = 1;
int pincerSpeed = 1;

Servo myservo1;  //Front left wheel
Servo myservo2;  //Back left wheel
Servo myservo3; //Front right wheel
Servo myservo4; //Back right wheel
Servo myservo5; //claw
Servo myservo6; //arm
Servo myservo7; //slider
Servo myservo8; //pincers
Servo myservo9;
Servo myservo10; 

void setup(){
  
  //6 is right back wheel, 7 is left back wheel, 8 is right front wheel, 9 is left front wheel
  //PWM control wheels

  myservo1.attach(9); //Front left wheel
  myservo2.attach(7); //Back left wheel
  myservo3.attach(8); //Front right wheel
  myservo4.attach(6); //Back right wheel

  myservo5.attach(3);
  myservo6.attach(4);
  myservo7.attach(5);
  
  myservo8.attach(11);
  myservo9.attach(12);
  myservo10.attach(13);

  Serial.begin(9600); //Serial output to computer
  Serial2.begin(9600); //Serial communication with RPi
  //delay(100);
    
  Wire.begin();
  //Put the HMC5883 IC into the correct operating mode
  Wire.beginTransmission(address); //open communication with HMC5883
  Wire.write(0x02); //select mode register
  Wire.write(0x00); //continuous measurement mode
  Wire.endTransmission();
}

void loop(){
  int x,y,z; //triple axis data
  //Tell the HMC5883 where to begin reading data
  Wire.beginTransmission(address);
  Wire.write(0x03); //select register 3, X MSB register
  Wire.endTransmission();
 
 //Read data from each axis, 2 registers per axis
  Wire.requestFrom(address, 6);
  if(6<=Wire.available()){
    //Serial.println("6 < wire");
    x = Wire.read()<<8; //X msb
    x |= Wire.read(); //X lsb
    z = Wire.read()<<8; //Z msb
    z |= Wire.read(); //Z lsb
    y = Wire.read()<<8; //Y msb
    y |= Wire.read(); //Y lsb
    
    angle = atan2(y,x);
    if(angle < 0){
      angle += 2*PI;
    }
    angle *= 180/PI;
    //angle += 360 - 13.24 - 257.45 + 30;
    
    if(angle > 360){
      angle -= 360;
    }
  }
  

  //Process string and build float array
  if(Serial2.available() > 0){
    data_index = 0;
    start = 0;
    String string = Serial2.readStringUntil('\n');
    //String string = "0.5,1.0,0.1,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0"; //Test String
    //Serial.println(string);

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
    
  horizontalSpeed = newData[0]; //Left/right joystick
  verticalSpeed = newData[1]; //Forward/backward joystick
  rotationSpeed = newData[2]; //Twist joystick
  dampingFactor = (newData[3]+1)/2; //Takes a number from [-1:1] and converts it to [0:1] to control speed range 
  }
  
  moveRover(verticalSpeed, horizontalSpeed, rotationSpeed);
  moveArm();
  moveClaw();
    
  //Send values to RPi
  Serial2.println(angle);
  
  //Print values to computer
  Serial.println(angle);
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
//  int motorspeed = custom_map(joystickSpeed);
//  if (joystickSpeed >= 0){
//    for (int i = 90; i <=motorSpeed; i++){
//      servo.write(i);
//      delay(1);
//    }
//  }
//  else if (joystickSpeed <= 0){
//    for (int i = 90; i >=motorSpeed; i--){
//      servo.write(i);
//      delay(1);
//    }
  servo.write(custom_map(joystickSpeed));
}

void moveRover(float verticalSpeed, float horizontalSpeed, float rotationSpeed){
  float turningSpeed = diagonalSpeed(verticalSpeed, horizontalSpeed);
  
  if(horizontalSpeed != 0 || verticalSpeed != 0){  //Continuous forward/backward/turning movement
    if (horizontalSpeed > 0){  //first and fourth quadrant
      actuate_motor(myservo3, turningSpeed); //Front left wheel moves faster than right wheels
      actuate_motor(myservo4, turningSpeed); //Back left wheel moves faster than right wheels
      actuate_motor(myservo1, turningSpeed*(1-abs(horizontalSpeed))); //Right wheel moves slower wrt left wheel
      actuate_motor(myservo2, turningSpeed*(1-abs(horizontalSpeed))); //Right wheel moves slower wrt left wheel
    }
    else{  //second and third quadrant
      actuate_motor(myservo3, turningSpeed*(1-abs(horizontalSpeed))); //Left wheel moves slower wrt right wheel
      actuate_motor(myservo4, turningSpeed*(1-abs(horizontalSpeed))); //Left wheel moves slower wrt right wheel
      actuate_motor(myservo1, turningSpeed); //Right wheel moves faster
      actuate_motor(myservo2, turningSpeed); //Right wheel moves faster
    }
  }
  else{  //Rotate rover about centre axis; only rotate on the spot if the joystick doesn't go forward or backward
    actuate_motor(myservo1, rotationSpeed);
    actuate_motor(myservo2, rotationSpeed);
    actuate_motor(myservo3, -rotationSpeed);
    actuate_motor(myservo4, -rotationSpeed);
  }
}

void moveArm(){
  if (newData[10]){//move claw down
    actuate_motor(myservo5, -clawSpeed);
  }
  else if (newData[11]){//move claw up
    actuate_motor(myservo5, clawSpeed);
  }
  else{
    actuate_motor(myservo5, 0);
  }
  if (newData[12]){//move arm down
    actuate_motor(myservo6, -armSpeed);
  }
  else if (newData[13]){//move arm up
    actuate_motor(myservo6, armSpeed);
  }   
  else{
    actuate_motor(myservo6, 0);
  }
  if (newData[14]){//move slider right
    actuate_motor(myservo7, -sliderSpeed);
  }
  else if (newData[15]){//move slider left
    actuate_motor(myservo7, sliderSpeed);
  }
  else{
    actuate_motor(myservo7, 0);
  }
}

void moveClaw(){
  if (newData[4]){//close claw
    actuate_servo(myservo8, pincerSpeed);
  }
  else if (newData[5]){//open claw
    actuate_servo(myservo8, -pincerSpeed);
  }
  if (newData[6]){
    actuate_servo(myservo9, -pincerSpeed);
  }
  else if (newData[8]){
    actuate_servo(myservo9, pincerSpeed);
  }
  if (newData[7]){
    actuate_servo(myservo10, -pincerSpeed);
  }
  else if (newData[9]){
    actuate_servo(myservo10, pincerSpeed);
  }
}

void actuate_servo(Servo servo, int servoSpeed){
  int servoAngle = servo.read();

  //Serial.println(servoAngle);
  if (servoAngle <= 180 && servoAngle >=0){
    servoAngle = servoAngle + servoSpeed;
    servo.write(servoAngle);
  }
}

float diagonalSpeed(float vy, float vx){
  float vz = sqrt(vx*vx+vy*vy);
  
  return (vy >=0 ? vz:-vz)/sqrt(2);  //Normalize speed for range [-1:1] and direction of vy
}
