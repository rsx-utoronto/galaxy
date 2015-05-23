int moistureSensor = 1;
int moistureValue = 0;
void setup() {
  Serial.begin(9600);
}

void loop() {
  int moistureValue = analogRead(moistureSensor);
  Serial.println(moistureValue); 
  delay(1000);        // delay 1 second between reads
}
