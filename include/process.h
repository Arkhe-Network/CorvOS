#ifndef PROCESS_H
#define PROCESS_H

int proc_create(void (*func)(), int priority);
void proc_schedule();
void proc_yield();
void proc_init();

#endif