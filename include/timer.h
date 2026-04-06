#ifndef TIMER_H
#define TIMER_H

void timer_init();
void timer_sleep(int seconds);
void timer_delay(int milliseconds);
void timer_set_alarm(int seconds);

#endif