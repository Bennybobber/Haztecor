void tempsetup() {
  digitalWrite(6,HIGH);     // pre-set output value to HIGH
  pinMode(6,OUTPUT);        // set to output, it will be HIGH
}

void temploop() {
  digitalWrite(6,LOW);
  delay(1000);
  digitalWrite(6,HIGH);
  delay(1000);
}
