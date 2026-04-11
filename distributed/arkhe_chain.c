#include <stdio.h>
#include <string.h>
#include <time.h>
#include "arkhe_chain.h"

#define MAX_BLOCKS 100
static Block chain[MAX_BLOCKS];
static int block_count = 0;

void arkhe_chain_init() {
    printf("Arkhe-Chain: Initializing (Genesis Block)...\n");
    arkhe_chain_add_block("Genesis Block - CorvOS Coherence Launch");
}

void arkhe_chain_add_block(const char *data) {
    if (block_count >= MAX_BLOCKS) return;

    Block *new_block = &chain[block_count];
    new_block->index = block_count;
    new_block->timestamp = (uint64_t)time(NULL);
    strncpy(new_block->data, data, 1023);
    new_block->data[1023] = '\0';

    if (block_count > 0) {
        strcpy(new_block->prev_hash, chain[block_count-1].hash);
    } else {
        strcpy(new_block->prev_hash, "0");
    }

    // Simple Merkle root simulation
    snprintf(new_block->merkle_root, 65, "merkle_root_%d", block_count);

    // Simple hash simulation
    snprintf(new_block->hash, 65, "hash_%d_%lu", block_count, new_block->timestamp);

    printf("Arkhe-Chain: Block %d added - Hash: %s\n", block_count, new_block->hash);
    block_count++;
}

void arkhe_chain_anchor_law(const char *law_data) {
    printf("Arkhe-Chain: ANCHORING NEW PHASE LAW...\n");
    char data[1024];
    snprintf(data, sizeof(data), "[LAW] %s", law_data);
    arkhe_chain_add_block(data);
}

void arkhe_chain_print() {
    printf("Arkhe-Chain (PoC): \n");
    for (int i = 0; i < block_count; i++) {
        printf("[%d] Time: %lu, Data: %s, Merkle: %s, Hash: %s\n",
               chain[i].index, chain[i].timestamp, chain[i].data, chain[i].merkle_root, chain[i].hash);
    }
}
