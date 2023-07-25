#ifndef HORIZONTAL_MOVEMENT_H
#define HORIZONTAL_MOVEMENT_H
#include <Arduino.h>

void byj_setup();

void move_right();
void move_left();
void step_right(int steps);
void step_left(int steps);
#endif
