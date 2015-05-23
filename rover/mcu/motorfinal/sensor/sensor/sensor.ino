/* MQ-4 Methane Sensor Circuit with Arduino */
#include <Wire.h> //I2C Arduino Library
#define address 0x1E //0011110b, I2C 7bit address of HMC5883
const int AOUTpin=0;//the AOUT pin of the methane sensor goes into analog pin A0 of the arduino
const int DOUTpin=5;//the DOUT pin of the methane sensor goes into digital pin D8 of the arduino
const int ledPin=13;//the anode of the LED connects to digital pin D13 of the arduino
float Ro = 10000.0;
float Vrl = 0.0;
float Rs = 0.0;
float ratio = 0.0;
float ppm = 0.0;
int limit;
int MethaneValue;
int moistureSensor = 1;
int moistureValue = 0;


void setup() {
  Serial.begin(9600);
  Serial2.begin(9600);//sets the baud rate
  
  pinMode(DOUTpin, INPUT);//sets the pin as an input to the arduino
  pinMode(ledPin, OUTPUT);//sets the pin as an output of the arduino
  
  Wire.begin();
  //Put the HMC5883 IC into the correct operating mode
  Wire.beginTransmission(address); //open communication with HMC5883
  Wire.write(0x02); //select mode register
  Wire.write(0x00); //continuous measurement mode
  Wire.endTransmission();
}

void loop()
{
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
  }
  
  MethaneValue= analogRead(AOUTpin);//reads the analaog MethaneValue from the methane sensor's AOUT pin
  limit= digitalRead(DOUTpin);//reads the digital MethaneValue from the methane sensor's DOUT pin
  Vrl = MethaneValue * ( 5.00 / 1024.0  );      // V
  Rs = 20000 * ( 5.00 - Vrl) / Vrl ;   // Ohm
  ratio =  Rs/Ro;
  ppm = get_CO(ratio);  
  moistureValue = analogRead(moistureSensor);
  
  
  Serial2.println("***********************Princess Ginger is stupid***************************");
  //Serial2.print("x: ");
  Serial2.print(x);
  Serial2.print(",");
  Serial2.print(y);
  Serial2.print(",");
  Serial2.print(z);
  
  Serial2.print(",");
  Serial2.print(ppm);//prints the methane MethaneValue
  Serial2.print(",");
  Serial2.print(ppm);//prints the methane MethaneValue
  Serial2.print(",");
  Serial2.print(ppm);//prints the methane MethaneValue
  
  Serial2.print(",");
  Serial2.print(moistureValue); 
  Serial2.print(",");
  Serial2.println(moistureValue); 

  
  Serial.print("x: ");
  Serial.print(x);
  Serial.print("  y: ");
  Serial.print(y);
  Serial.print("  z: ");
  Serial.println(z);
  
  delay(250);
  Serial.print("Methane MethaneValue: ");
  Serial.println(MethaneValue);//prints the methane MethaneValue
  Serial.print("Limit: ");
  Serial.println(limit);//prints the limit reached as either LOW or HIGH (above or underneath)
  Serial.print("ppm: ");
  Serial.println(ppm);//prints the limit reached as either LOW or HIGH (above or underneath)

  Serial.print("Soil Moisture: ");
  Serial.println(moistureValue); 

  //Serial.write(AOUTpin);
  delay(250);
}


float get_CO (float ratio){
  float ppm = 0.0;
  ppm = 37143 * pow (ratio, -3.178);
  return ppm;
}
