

// Returns the sensors vlaues from analog
int returnTemp()
{
  int reading = analogRead(A0);
  float voltage = reading * 3.3;
  voltage /= 1024.0;
  int temperatureC = (voltage - 0.5) * 100; 
  return temperatureC;
}
