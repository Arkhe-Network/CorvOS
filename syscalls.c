#include <stdio.h>
#include <stdlib.h>
#include "../include/console.h"

// System Calls for CorvOS
// Simple syscall interface

void sys_write(const char *str) {
    console_write(str);
}

int sys_read(char *buffer, int len) {
    // Simulate read
    return 0;
}

void sys_exit() {
    exit(0);
}