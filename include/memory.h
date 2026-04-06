#ifndef MEMORY_H
#define MEMORY_H

#include <stddef.h>

void mm_init();
void *mm_alloc(size_t size);
void mm_free(void *ptr);

#endif