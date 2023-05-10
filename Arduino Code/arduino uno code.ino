#include <SoftwareSerial.h>
#include <ThingSpeak.h>

#define trigPin 9
#define echoPin 10

// Define ThingSpeak parameters
char ssid[] = "TheTest";
char pass[] = "password";
unsigned long channelID = 2102276;
const char *writeAPIKey = "SEH46J6SXYACJX83";

// Define variables
long duration, cm;

void setup()
{
  Serial.begin(9600);
  ThingSpeak.begin(client);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop()
{
  // Send a pulse to the ultrasonic sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // calculate distance in cm
  duration = pulseIn(echoPin, HIGH);
  cm = duration / 58;

  // Print distance to serial monitor
  Serial.print("Distance: ");
  Serial.print(cm);
  Serial.println(" cm");

  // Send data to ThingSpeak
  ThingSpeak.setField(3, (cm < 20 ? 1 : 0)); // If distance < 20cm, set field 3 to 1, else set to 0
  int status = ThingSpeak.writeFields(channelID, writeAPIKey);
  if (status == 200)
  {
    Serial.println("Data sent to ThingSpeak successfully.");
  }
  else
  {
    Serial.println("Problem sending data to ThingSpeak.");
  }

  delay(5000); // Wait 5 seconds before taking another measurement
}