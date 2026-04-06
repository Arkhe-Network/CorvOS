#ifndef SIMPLEFS_H
#define SIMPLEFS_H

void fs_init();
int fs_create(const char *name);
int fs_write(int fd, const char *data, int len);
int fs_read(int fd, char *buffer, int len);

#endif