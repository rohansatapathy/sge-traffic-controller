#include <stdlib.h>
#define LED_PIN 12

int incomingByte = 0;


void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  incomingByte = Serial.read();
  if (incomingByte == 't') {
    digitalWrite(LED_PIN, HIGH);
  } else {
    digitalWrite(LED_PIN, LOW);
  }
  while (Serial.available() <= 0) {}
}
