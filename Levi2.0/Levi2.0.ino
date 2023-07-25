#include "vertical_movement.h"
#include "horizontal_movement.h"
#include "pen_movement.h"

void setup() {

  nema_setup();
  byj_setup();
  pen_setup();
  Serial.setTimeout(20);
  Serial.begin(9600);
  delay(1000);
}

void loop() {

// for(int i = 0; i < 30; i++){
//
//  step_left(25);
//  delay(500);
//  pen_point(62);
//  delay(500);
// }

 for(int i = 0; i < 30; i++){

  vertical_down(250, 1000); //800
  delay(1000);
  pen_point(60);
  delay(500);
 }

 while(1);

  

}
