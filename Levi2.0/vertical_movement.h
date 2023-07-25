#ifndef VERTICAL_MOVEMENT_H
#define VERTICAL_MOVEMENT_H
#include <Arduino.h> //necessary lib to import for arduino apps such as OUTPUT type 

void nema_setup();
void vertical_up(int steps, int ver_delay);
void vertical_down(int steps, int ver_delay);

#endif
