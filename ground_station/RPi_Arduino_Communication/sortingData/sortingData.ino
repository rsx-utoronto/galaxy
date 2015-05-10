int newData[200]; //We will know the size of the float array
int start = 0; //start keeps track of next float in string to be parsed
int data_index = 0; //data_index keeps track of which index to place float in float array

void setup(){
  Serial.begin(9600);
  Serial2.begin(9600);
  delay(500);
}

void loop(){
  //Process string and build float array
  if(Serial2.available() > 0){

    String string = Serial2.readStringUntil('\n');

    Serial.print(string);

    /*
    for(int i = 0; i < string.length(); i++){
      if(string.substring(i, i+1) == "," || i == string.length()-1){
        if (string.substring(i, i+1) == ","){ //Check for comma to denote end of float in string
          String temp = string.substring(start, i);
          newData[data_index] = temp.toInt();
        }
        else{ //Account for last float in string
          String temp = string.substring(start, string.length());
          newData[data_index] = temp.toInt();
        }
        start = i+1;
        data_index++;
      }
    }

    //Print parsed example float array
    for(int i = 0; i < 10; i++){
      Serial.print(newData[i]);
      Serial.print(" ");
    }

    //Serial.flush();*/
    Serial.println("");
  }
}



