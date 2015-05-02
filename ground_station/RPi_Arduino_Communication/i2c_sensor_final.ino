#include <Wire.h>
#define SLAVE_ADDRESS 0x2A

//SDA on pi = pin 3;
//SCL on pi = pin 5;
//GND on pi = pin 6;
//Voltage pulled up to 3.3V using a 4.7K resistor on the SDA and SCL lines
//Using an arduino mega...

int input, temp, temp2;

boolean analog = false;
int rec;
int map_table[53];
int index = 0;

void setup() {
    // initialize i2c as slave
    
    Wire.begin(SLAVE_ADDRESS);
    Wire.onRequest(sendData);
    Wire.onReceive(receiveData);
    
    map_table[0] = A0;
    map_table[1] = A1;
    map_table[2] = A2;
    map_table[3] = A3;
    map_table[4] = A4;
    map_table[5] = A5;
    map_table[6] = A6;
    map_table[7] = A7;
    map_table[8] = A8;
    map_table[9] = A9;
    map_table[10] = A10;
    map_table[11] = A11;
    map_table[12] = A12;
    map_table[13] = A13;
    map_table[14] = A14;
    map_table[15] = A15;
    map_table[16] = A0;
    map_table[17] = A0;
    map_table[18] = A0;
    map_table[19] = A0;
    map_table[20] = A0;
    map_table[21] = A0;
    map_table[22] = 22;
    map_table[23] = 23;
    map_table[24] = 24;
    map_table[25] = 25;
    map_table[26] = 26;
    map_table[27] = 27;
    map_table[28] = 28;
    map_table[29] = 29;
    map_table[30] = 30;
    map_table[31] = 31;
    map_table[32] = 32;
    map_table[33] = 33;
    map_table[34] = 34;
    map_table[35] = 35;
    map_table[36] = 36;
    map_table[37] = 37;
    map_table[38] = 38;
    map_table[39] = 39;
    map_table[40] = 40;
    map_table[41] = 41;
    map_table[42] = 42;
    map_table[43] = 43;
    map_table[44] = 44;
    map_table[45] = 45;
    map_table[46] = 46;
    map_table[47] = 47;
    map_table[48] = 48;
    map_table[49] = 49;
    map_table[50] = 50;
    map_table[51] = 51;
    map_table[52] = 52;
    map_table[53] = 53;
    Serial.begin(9600);
}


void loop() {
    if (analog)
      input = analogRead(map_table[rec]);
    else
      input = digitalRead(map_table[rec]);
  Serial.println (input);
  delay(50);
}

// callback for sending data
// note: we need to send the data one byte at a time, so in order to send integers, we are send 4 data packets in a row (the pi asks for 4 packets in a row)
void sendData() { 
    if (index ==0){
      Wire.write(input);
      index++;
    }
    else if (index ==1)
    {
      Wire.write(input>>8);
      index++;
    }
    else if (index ==2)
    {
      Wire.write(input>>16);s
      index++;
    }
    else
    {
      Wire.write(input>>24);
      index = 0;
    }
}

void receiveData(int numBytes){

  rec = Wire.read();
  if (rec<= 15)
    analog = true;
  else
    analog = false;
  
}
