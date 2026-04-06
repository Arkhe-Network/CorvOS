#ifndef BIGTABLE_H
#define BIGTABLE_H

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

void bigtable_init(BigtableTable *table);
void bigtable_put(BigtableTable *table, char *row_key, char *cf, char *cq, char *value);
char *bigtable_get(BigtableTable *table, char *row_key, char *cf, char *cq);

#endif