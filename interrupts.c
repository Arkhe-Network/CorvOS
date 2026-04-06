#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

// Interrupt Handling for CorvOS
// Simulated interrupts using signals

void interrupt_handler(int sig) {
    printf("Interrupt received: %d\n", sig);
    // Handle interrupt, e.g., schedule or yield
    // For demo, just print
}

void interrupts_init() {
    signal(SIGINT, interrupt_handler);  // Ctrl+C
    signal(SIGALRM, interrupt_handler); // Timer
    printf("Interrupt System Initialized\n");
}