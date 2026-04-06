#include <stdio.h>
#include <stdlib.h>
#include <setjmp.h>

// Simple Process Manager for CorvOS
// Basic process creation and scheduling with context switching

#define MAX_PROCESSES 10

typedef enum { READY, RUNNING, BLOCKED } ProcessState;

typedef struct {
    int pid;
    ProcessState state;
    jmp_buf context;
    void (*entry_point)();
    int priority; // Higher number = higher priority
} PCB;

PCB processes[MAX_PROCESSES];
int process_count = 0;
int current_pid = 0;
jmp_buf scheduler_context;

void proc_yield() {
    if (setjmp(processes[current_pid].context) == 0) {
        longjmp(scheduler_context, 1);
    }
}

void proc_schedule() {
    static int current = 0;
    if (process_count == 0) return;

    // Save current context
    if (setjmp(scheduler_context) == 0) {
        processes[current].state = READY;
        current = (current + 1) % process_count;
        processes[current].state = RUNNING;
        printf("Switching to process %d\n", processes[current].pid);
        longjmp(processes[current].context, 1);
    }
}

int proc_create(void (*func)(), int priority) {
    if (process_count >= MAX_PROCESSES) return -1;
    processes[process_count].pid = current_pid++;
    processes[process_count].state = READY;
    processes[process_count].entry_point = func;
    processes[process_count].priority = priority;
    return process_count++;
}

void proc_init() {
    process_count = 0;
    current_pid = 1;
    printf("Process Manager with Context Switching Initialized\n");
}