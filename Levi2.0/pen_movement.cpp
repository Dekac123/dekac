
#include <Servo.h>
#include "pen_movement.h"

Servo myservo; 


void pen_setup() {
  myservo.attach(6); 
  delay(100);
  myservo.write(180); 
}

void pen_point(int dist) {

  for (int pos = 180; pos >= dist; pos -= 1) { 
    myservo.write(pos);              
    delay(10);                       
  }
  
  for (int pos = dist; pos <= 180; pos += 1) { 
    myservo.write(pos);            
    delay(10);                       
  }
  
  
}
