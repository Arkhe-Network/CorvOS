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
    float lambda_2; // Coherence factor
    int phase_slice; // Phase-based time slice
    int started;
} PCB;

PCB processes[MAX_PROCESSES];
int process_count = 0;
int current_process_idx = -1;
jmp_buf scheduler_context;

void proc_yield() {
    if (current_process_idx == -1) return;
    if (setjmp(processes[current_process_idx].context) == 0) {
        longjmp(scheduler_context, 1);
    }
}

void proc_schedule() {
    if (process_count == 0) return;

    // Save current context
    if (setjmp(scheduler_context) == 0) {
        if (current_process_idx != -1) {
            processes[current_process_idx].state = READY;
        }

        // Phase-based scheduling: find the process with the highest lambda_2
        // Use round-robin as a tie-breaker for same coherence
        int start = (current_process_idx + 1) % process_count;
        int best = -1;
        float max_lambda = -1.0f;
        for (int i = 0; i < process_count; i++) {
            int idx = (start + i) % process_count;
            if (processes[idx].lambda_2 > max_lambda) {
                max_lambda = processes[idx].lambda_2;
                best = idx;
            }
        }

        if (best != -1) current_process_idx = best;
        else current_process_idx = 0;

        processes[current_process_idx].state = RUNNING;
        printf("Phase Scheduler: Switching to process %d (lambda_2: %.3f)\n",
               processes[current_process_idx].pid, processes[current_process_idx].lambda_2);

        if (!processes[current_process_idx].started) {
            processes[current_process_idx].started = 1;
            processes[current_process_idx].entry_point();
            // If the process returns, mark it as finished or just loop it
            printf("Process %d finished execution\n", processes[current_process_idx].pid);
            longjmp(scheduler_context, 1);
        } else {
            longjmp(processes[current_process_idx].context, 1);
        }
    }
}

static int global_pid_counter = 1;

int proc_create(void (*func)(), int priority) {
    if (process_count >= MAX_PROCESSES) return -1;
    processes[process_count].pid = global_pid_counter++;
    processes[process_count].state = READY;
    processes[process_count].entry_point = func;
    processes[process_count].priority = priority;
    processes[process_count].lambda_2 = 0.95f; // Initial coherence
    processes[process_count].phase_slice = 100;
    processes[process_count].started = 0;
    return process_count++;
}

void proc_init() {
    process_count = 0;
    current_process_idx = -1;
    global_pid_counter = 1;
    printf("Process Manager with Context Switching Initialized\n");
}