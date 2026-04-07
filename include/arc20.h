#ifndef ARC20_H
#define ARC20_H

#include <stdint.h>

typedef struct {
    char name[32];
    char symbol[8];
    uint64_t total_supply; // Using uint64_t for simulation
    float lambda_collateral;
} ARC20Token;

void arc20_init(ARC20Token *token, const char *name, const char *symbol);
void arc20_mint_based_on_coherence(ARC20Token *token, float lambda_proof);
void arc20_print_status(ARC20Token *token);

#endif
