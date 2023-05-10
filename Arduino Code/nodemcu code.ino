#include <ESP8266WiFi.h>
#include <ThingSpeak.h>
#include <HX711.h>

const char *ssid = "TheTest";
const char *password = "password";

const char *server = "api.thingspeak.com";
const char *apiKey = "SEH46J6SXYACJX83";
const unsigned long channelId = 2102276;

WiFiClient client;

void setup()
{
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to Wi-Fi...");
  }
  Serial.println("Connected to Wi-Fi!");

  ThingSpeak.begin(client);

  pinMode(D5, INPUT);
}

void loop()
{
  int tiltData = digitalRead(D5);

  if (tiltData == LOW)
  {
    float loadCellData = hx711.get_units(10);
    Serial.println(loadCellData);
    ThingSpeak.writeField(channelId, 2, loadCellData, apiKey);
  }

  delay(15000);
}