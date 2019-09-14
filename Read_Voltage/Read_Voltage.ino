

int ledPin = 7;
void setup() {
  // initialize serial communication at 9600 bits per second:
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);

  //Serial.begin(9600);// unity
  Serial.begin(57600); //The c++ one 

}

// the loop routine runs over and over again forever:
void loop() {    
  // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  float v1 = analogRead(A0) * (1.0 / 1023.0);
  float v2 = analogRead(A1) * (1.0 / 1023.0);
  float v3 = analogRead(A2) * (1.0 / 1023.0);
  float v4 = analogRead(A3) * (1.0 / 1023.0);
  /*
  int v1 = analogRead(A0);
  int v2 = analogRead(A1);
  int v3 = analogRead(A2);
  int v4 = analogRead(A3);
  */
  
  // print out the value you read:
 /* if(v1 > 1)
    digitalWrite(ledPin, LOW);
  else
     digitalWrite(ledPin, HIGH);*/
//if output window here
// goes for the just ardunio one

  //Serial.print(" ");
  Serial.print(v1);
  Serial.print(",");
  Serial.print(v2);
  Serial.print(",");
  Serial.print(v3);
  Serial.print(",");
  Serial.println(v4);

//
//if serial output
// goes for unity one
//
/*
 Serial.print("a");
  Serial.print(v1);
  Serial.print(",");
  Serial.print(v2);
  Serial.print(",");
  Serial.print(v3);
  Serial.print(",");
  Serial.print(v4);
  Serial.println("b");
*/
//
/*
  Serial.print(v1);
  Serial.print(",");
  Serial.print(v2);
  Serial.print(",");
  Serial.print(v3);
  Serial.print(",");
  Serial.println(v4);
 */
}
