#include <Servo.h>

Servo trackSystem;
Servo trigger2; 



int trigPin = 11;
int echoPin = 5;
Servo lowerMotor;

int trackPos, triggerPos = 0;

const int n = 20;
float duration = 0.0;
float distance = 0.0;

void moveServo(){
  // goes from 0 degrees to 180 degrees in steps of 1 degree
  // tell servo to go to position in variable 'pos'
  // waits 15 ms for the servo to reach the position
  for (int pos = 0; pos <= 360; ++pos) { 
    trackSystem.write(pos);
    trigger2.write(pos);
    delay(15);
  }
}

void setup() {
  pinMode(8,OUTPUT);
  lowerMotor.attach(8);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Serial.begin(9600);
  Serial.println(1);
}

void loop() {
  motorControl(180);

  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = (duration/2) / 29.1;
  Serial.print("Distance: ");
  Serial.println(distance);
  // if (distance < 6) {
  //   delay(100);
  //   // for (int pos = 0; pos <= 400; pos += 1) { // goes from 0 degrees to 180 degrees
  //   //   myservo.write(pos);              // tell servo to go to position in variable 'pos'
  //   //   delay(n);                       // waits 15 ms for the servo to reach the position
  //   // }
  //   Serial.print("Stopped.");
  //   while (1) {}
  // }
  delay(100);
}

int motorControl(int value){
  lowerMotor.write(map(value,0,1000,0,100));
}