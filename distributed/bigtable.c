#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Simplified Bigtable Implementation for CorvOS
// Based on https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf

typedef struct {
    char *row_key;
    char *column_family;
    char *column_qualifier;
    char *value;
    long timestamp;
} BigtableEntry;

typedef struct {
    BigtableEntry *entries;
    int size;
    int capacity;
} BigtableTable;

void bigtable_init(BigtableTable *table) {
    table->entries = malloc(sizeof(BigtableEntry) * 10);
    table->size = 0;
    table->capacity = 10;
    printf("Bigtable Table Initialized\n");
}

void bigtable_put(BigtableTable *table, char *row_key, char *cf, char *cq, char *value) {
    if (table->size >= table->capacity) {
        table->capacity *= 2;
        table->entries = realloc(table->entries, sizeof(BigtableEntry) * table->capacity);
    }
    BigtableEntry *entry = &table->entries[table->size++];
    entry->row_key = strdup(row_key);
    entry->column_family = strdup(cf);
    entry->column_qualifier = strdup(cq);
    entry->value = strdup(value);
    entry->timestamp = time(NULL); // Simplified
    printf("Put entry: %s:%s:%s = %s\n", row_key, cf, cq, value);
}

char *bigtable_get(BigtableTable *table, char *row_key, char *cf, char *cq) {
    for (int i = 0; i < table->size; i++) {
        BigtableEntry *entry = &table->entries[i];
        if (strcmp(entry->row_key, row_key) == 0 &&
            strcmp(entry->column_family, cf) == 0 &&
            strcmp(entry->column_qualifier, cq) == 0) {
            return entry->value;
        }
    }
    return NULL;
}