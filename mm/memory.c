#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Simple Memory Manager for CorvOS
// Basic heap allocation

#define HEAP_SIZE 1024 * 1024  // 1MB heap
static char heap[HEAP_SIZE];
static int heap_used = 0;

void *mm_alloc(size_t size) {
    if (heap_used + size > HEAP_SIZE) return NULL;
    void *ptr = &heap[heap_used];
    heap_used += size;
    return ptr;
}

void mm_free(void *ptr) {
    // Simple free: no deallocation, just mark as unused (placeholder)
    // In a real OS, implement proper free
    printf("Free called on %p (placeholder)\n", ptr);
}

void mm_init() {
    heap_used = 0;
    printf("Memory Manager Initialized\n");
}