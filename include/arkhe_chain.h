#ifndef ARKHE_CHAIN_H
#define ARKHE_CHAIN_H

#include <stdint.h>

typedef struct {
    uint32_t index;
    uint64_t timestamp;
    char data[1024];
    char prev_hash[65];
    char merkle_root[65];
    char hash[65];
} Block;

void arkhe_chain_init();
void arkhe_chain_add_block(const char *data);
void arkhe_chain_anchor_law(const char *law_data);
void arkhe_chain_print();

#endif
