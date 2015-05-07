String string = "1,2,3,4,5,6,7,8,9.5,10.11"; //Example string to be parsed
float newData[10]; //We will know the size of the float array
int start = 0; //start keeps track of next float in string to be parsed
int data_index = 0; //data_index keeps track of which index to place float in float array

void setup(){
  Serial.begin(9600);
  Serial.println(string);
  delay(500);
}

void loop(){
  //Process string and build float array
  for(int i = 0; i < string.length(); i++){
    if(string.substring(i, i+1) == "," || i == string.length()-1){
      if (string.substring(i, i+1) == ","){ //Check for comma to denote end of float in string
        newData[data_index] = string.substring(start, i).toFloat();
      }else{ //Account for last float in string
        newData[data_index] = string.substring(start, string.length()).toFloat();
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
  
  END:
  goto END;
}
