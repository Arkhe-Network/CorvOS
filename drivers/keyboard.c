#include <stdio.h>
#include <stdlib.h>
#ifdef __linux__
#include <ncurses.h>
#endif

// Keyboard Driver for CorvOS
// Real hardware input using ncurses

void keyboard_init() {
    printf("Keyboard Driver Initialized (simulated)\n");
}

char keyboard_read() {
    // Standard blocking read for interactivity
    char c;
    if (scanf("%c", &c) == 1) return c;
    return 0;
}

void keyboard_close() {
}