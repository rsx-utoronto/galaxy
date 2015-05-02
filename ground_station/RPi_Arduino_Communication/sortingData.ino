#include String.h
String string = "1,2,3,4,5,6,7,8,9,10,11.5";
float newData[11];
int length = 25;

void setup(){
  Serial.begin(9600);
}

/*String input = "123,456";
int firstVal, secondVal;
 
for (int i = 0; i < input.length(); i++) {
  if (input.substring(i, i+1) == ",") {
    firstVal = input.substring(0, i).toInt();
    secondVal = input.substring(i+1).toInt();
    break;
  }
}*/

void loop(){
  Serial.println(string.substring(2,3));
  
//  for(int i = 0; i < length; i++){
//    char c = string[i];
//    if(c == ','){
//      continue;
//    }else{
//      *newString = c;
//      if (i < length){
//        next = string[i+1];
//        if (next != ','){
//          *newString = *newString + next;//'1'+0' = "10"
//        }
//      }
//    }
//  }
  
//  int start = 0;
//  int data_index = 0;
//  for(int i = 0; i < length; i++){
//    if (string.substring(i, i+1) == ",") {
//      newData[data_index] = string.substring(start, i).toFloat();
//      start = i+1;
//      data_index++;
//    }
//  }

  char str[] = "0.5";
  
  String.toCharArray(str, 10);
  float pH = atof(str);
  Serial.println(f);
  
    END:
    goto END;
}
