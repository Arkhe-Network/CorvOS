#ifndef SPANNER_H
#define SPANNER_H

typedef struct {
    char *key;
    char *value;
} SpannerRecord;

typedef struct {
    SpannerRecord *records;
    int size;
    int capacity;
} SpannerDB;

void spanner_init(SpannerDB *db);
void spanner_write(SpannerDB *db, char *key, char *value);
char *spanner_read(SpannerDB *db, char *key);
void spanner_transaction(SpannerDB *db, void (*txn_func)(SpannerDB *));

#endif