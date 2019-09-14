int ledPin = 7;
void setup() {
  // initialize serial communication
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);

  Serial.begin(57600);
}

void loop() {
  float v1,v2,v3,v4;

  v1 = analogRead(A0) * (1.0 / 1023.0) * 5.0;
  v2 = analogRead(A1) * (1.0 / 1023.0) * 5.0;
  v3 = analogRead(A2) * (1.0 / 1023.0) * 5.0;
  v4 = analogRead(A3) * (1.0 / 1023.0) * 5.0;

  Serial.print('a');
  Serial.print(v1);
  Serial.print(',');
  Serial.print(v2);
  Serial.print(',');
  Serial.print(v3);
  Serial.print(',');
  Serial.print(v4);
  Serial.println('b');
}
