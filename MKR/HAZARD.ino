/*
  This is the main class and the start of the program,
  This starts the webserver,
*/

//Including the required header files/
#include <ArduinoHttpClient.h>
#include <WiFiNINA.h>
#include "arduino_secrets.h"
#include "geigerCounter.h"
#include <Wire.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#define ONE_WIRE_BUS 2

//Init global variables for the scope of the program.
char ssid[] = SECRET_SSID;
char pass[] = SECRET_PASS;
char username[] = SECRET_USERNAME;
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
char serverAddress[] = "192.168.194.41"; // server address
int port = 5000;
WiFiClient wifi;
WebSocketClient client = WebSocketClient(wifi, serverAddress, port);
int status = WL_IDLE_STATUS;
int count = 0;
int reading = 0;
float voltage = 0;
int temp = 0;
String json = "";

//Start of program
void setup()
{
  Serial.begin(9600);

  while (status != WL_CONNECTED)
  {
    status = WiFi.begin(ssid, pass);
  }

  IPAddress ip = WiFi.localIP();
  setupGeiger();
  sensors.begin();
}
//Starts the loop 
void loop()
{
  client.begin(); //begins connection to the client.
  while (client.connected())
  {
    loopGeiger();
    sensors.requestTemperatures(); 
    temp = sensors.getTempCByIndex(0);
    int reading = analogRead(A6);
    Serial.println(temp);
    delay(100);
    String temps = String(temp);
    String cpms = String(cpm);
    client.beginMessage(TYPE_TEXT);
    client.print("{\"cpm\":\"" + cpms + "\",\"temp\":\"" + temps + "\",\"light\":\"" + reading + "\"}"); //Sends the sensor data as a JSON object.
    client.endMessage();
    delay(50);
  }

  Serial.println("disconnected");
}
