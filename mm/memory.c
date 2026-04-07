#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Simple Memory Manager for CorvOS
// Basic heap allocation

#define HEAP_SIZE 1024 * 1024  // 1MB heap
static char heap[HEAP_SIZE];
static int heap_used = 0;

// Coherent Memory regions
#define COHERENT_REGION_SIZE 1024 * 64 // 64KB regions
static char coherent_memory[COHERENT_REGION_SIZE];
static int coherent_used = 0;

void *mm_alloc(size_t size) {
    if (heap_used + size > HEAP_SIZE) return NULL;
    void *ptr = &heap[heap_used];
    heap_used += size;
    return ptr;
}

void *mm_alloc_coherent(size_t size) {
    if (coherent_used + size > COHERENT_REGION_SIZE) return NULL;
    void *ptr = &coherent_memory[coherent_used];
    coherent_used += size;
    printf("Allocated coherent memory at %p\n", ptr);
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