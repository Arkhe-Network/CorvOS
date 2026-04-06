#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

// Timer Driver for CorvOS
// Real timing with alarm signals

void timer_handler(int sig) {
    printf("Timer interrupt\n");
    // Could trigger scheduling
}

void timer_init() {
    signal(SIGALRM, timer_handler);
    printf("Timer Driver Initialized (alarm)\n");
}

void timer_sleep(int seconds) {
    sleep(seconds);
}

void timer_delay(int milliseconds) {
    usleep(milliseconds * 1000);
}

void timer_set_alarm(int seconds) {
    alarm(seconds);
}