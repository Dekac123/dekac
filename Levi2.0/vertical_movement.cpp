#include "vertical_movement.h"


const int stepPin = 3; 
const int dirPin = 4; 
 
void nema_setup() {
  // Sets the two pins as Outputs
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);

}
void vertical_up(int steps, int ver_delay) {

  digitalWrite(dirPin,LOW); // Enables the motor to move in a particular direction
  // Makes 200 pulses for making one full cycle rotation
  for(int x = 0; x < steps; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(ver_delay); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(ver_delay); 
  }
}
void vertical_down(int steps, int ver_delay) {
  
  digitalWrite(dirPin,HIGH); //Changes the rotations direction
  // Makes 400 pulses for making two full cycle rotation
  for(int x = 0; x < steps; x++) {
    digitalWrite(stepPin,HIGH);
    delayMicroseconds(ver_delay);
    digitalWrite(stepPin,LOW);
    delayMicroseconds(ver_delay);
  }

}
