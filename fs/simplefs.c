#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Simple File System (RamDisk) for CorvOS
// Basic in-memory file system

#define MAX_FILES 100
#define MAX_FILE_SIZE 1024

typedef struct {
    char name[256];
    char data[MAX_FILE_SIZE];
    int size;
} File;

File files[MAX_FILES];
int file_count = 0;

void fs_init() {
    file_count = 0;
    printf("SimpleFS Initialized\n");
}

int fs_create(const char *name) {
    if (file_count >= MAX_FILES) return -1;
    strcpy(files[file_count].name, name);
    files[file_count].size = 0;
    return file_count++;
}

int fs_write(int fd, const char *data, int len) {
    if (fd < 0 || fd >= file_count) return -1;
    if (len > MAX_FILE_SIZE) len = MAX_FILE_SIZE;
    memcpy(files[fd].data, data, len);
    files[fd].size = len;
    return len;
}

int fs_read(int fd, char *buffer, int len) {
    if (fd < 0 || fd >= file_count) return -1;
    if (len > files[fd].size) len = files[fd].size;
    memcpy(buffer, files[fd].data, len);
    return len;
}