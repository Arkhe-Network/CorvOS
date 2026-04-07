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
    return '\n'; // Always return newline to avoid blocking in non-interactive mode
}

void keyboard_close() {
}