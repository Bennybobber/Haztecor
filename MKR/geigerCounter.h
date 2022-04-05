
#define LOG_PERIOD 15000 // Period of time which the data is logged.

#define MAX_PERIOD 60000 // 60 second Max period, allows for counts per min.

unsigned long counts; // Counts Times it clicks.

int cpm; // variable for CPM

unsigned int multiplier; // variable for calculation CPM in this sketch

unsigned long previousMillis; // variable for time measurement

// Adds one to count everytime the Geiger is triggered.
void tube_impulse()
{

  counts++;
}

//Sets up geiger and sets variables needed for use.
void setupGeiger()
{ 

  counts = 0;

  cpm = 0;

  multiplier = MAX_PERIOD / LOG_PERIOD; // calculating multiplier, depend on your log period

  // Serial.begin(9600);
  pinMode(4, INPUT);
  attachInterrupt(digitalPinToInterrupt(4), tube_impulse, FALLING); // define external interrupts
  //
  // Serial.println("Start counter"); // code I added
}

void loopGeiger()
{ // main cycle

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis > LOG_PERIOD)
  {

    previousMillis = currentMillis;

    cpm = counts * multiplier;

    counts = 0;
  }
}
