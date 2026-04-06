#include <stdio.h>
#include <stdlib.h>

// Simple Console Driver for CorvOS
// Provides basic output functionality

void console_init() {
    printf("Console Driver Initialized\n");
}

void console_write(const char *str) {
    printf("%s", str);
}

void console_writeln(const char *str) {
    printf("%s\n", str);
}