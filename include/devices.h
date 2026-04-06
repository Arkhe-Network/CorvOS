#ifndef DEVICES_H
#define DEVICES_H

void device_register(const char *name, void (*init)(), void (*read)(void*), void (*write)(void*));
void device_init_all();

#endif