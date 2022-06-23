#include <Arduino.h>
#include <Servo.h>

Servo porta;

void porta_motor();
void correctsound();
void incorrectsound();

String open_door;
#define portapin 10
#define piezzo 9
#define Green 11


void setup() {
  pinMode(piezzo, OUTPUT);
  pinMode(Green, OUTPUT);
  //digitalWrite(12, HIGH);
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(3, OUTPUT);
  
}

void loop() {
  open_door = Serial.readStringUntil('\n');
  if (open_door[0] == '1') {
    digitalWrite(3,LOW);
    delay(50);
    digitalWrite(3,HIGH);
  }
}

void porta_motor() {
  porta.attach(portapin);
  int i = 0;
  correctsound();
  digitalWrite(Green, HIGH);
  for (i = 0; i <= 90; i++) {
    porta.write(i);
    delay(10);
  }
  porta.detach();
  delay(5000);
  porta.attach(portapin);
  for (i; i >= 0; i--) {
    porta.write(i);
    delay(10);
  }
    digitalWrite(Green, LOW);
    porta.detach();
}


void correctsound() 
{
  digitalWrite(Green, HIGH);
  tone(piezzo, 600);
  delay(400);
  tone(piezzo, 800);
  delay(400);
  noTone(piezzo);
  digitalWrite(Green, LOW);
}

void incorrectsound()
{
  tone(piezzo, 300);
  delay(1000);
  noTone(piezzo);
}