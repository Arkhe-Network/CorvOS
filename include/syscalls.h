#ifndef SYSCALLS_H
#define SYSCALLS_H

void sys_write(const char *str);
int sys_read(char *buffer, int len);
void sys_exit();

#endif