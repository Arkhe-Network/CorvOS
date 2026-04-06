#include <stdio.h>
#include <stdlib.h>

// Device Manager for CorvOS
// Manage hardware devices

#define MAX_DEVICES 10

typedef struct {
    char name[32];
    void (*init)();
    void (*read)(void *data);
    void (*write)(void *data);
} Device;

Device devices[MAX_DEVICES];
int device_count = 0;

void device_register(const char *name, void (*init)(), void (*read)(void*), void (*write)(void*)) {
    if (device_count >= MAX_DEVICES) return;
    strcpy(devices[device_count].name, name);
    devices[device_count].init = init;
    devices[device_count].read = read;
    devices[device_count].write = write;
    device_count++;
}

void device_init_all() {
    for (int i = 0; i < device_count; i++) {
        if (devices[i].init) devices[i].init();
    }
    printf("Device Manager Initialized\n");
}