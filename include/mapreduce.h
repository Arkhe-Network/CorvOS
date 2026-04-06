#ifndef MAPREDUCE_H
#define MAPREDUCE_H

typedef struct {
    char *key;
    char *value;
} KeyValue;

typedef void (*MapFunc)(char *input, KeyValue **output, int *output_size);
typedef void (*ReduceFunc)(char *key, KeyValue *values, int value_count, KeyValue **output, int *output_size);

void mapreduce_execute(char *input, MapFunc map, ReduceFunc reduce);
void example_map(char *input, KeyValue **output, int *output_size);
void example_reduce(char *key, KeyValue *values, int value_count, KeyValue **output, int *output_size);

#endif