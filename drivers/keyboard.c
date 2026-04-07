#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>

// Keyboard Driver for CorvOS
// Real hardware input using non-blocking read

void keyboard_init() {
    // Set stdin to non-blocking
    int flags = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, flags | O_NONBLOCK);
    printf("Keyboard Driver Initialized (Non-blocking STDIN)\n");
}

char keyboard_read() {
    char c;
    if (read(STDIN_FILENO, &c, 1) == 1) return c;
    return 0;
}

void keyboard_close() {
}