#include <stdio.h>
#include <string.h>
#include "arc20.h"

void arc20_init(ARC20Token *token, const char *name, const char *symbol) {
    strncpy(token->name, name, 31);
    strncpy(token->symbol, symbol, 7);
    token->total_supply = 0;
    token->lambda_collateral = 0.0f;
    printf("ARC-20 Token Initialized: %s (%s)\n", name, symbol);
}

void arc20_mint_based_on_coherence(ARC20Token *token, float lambda_proof) {
    if (lambda_proof < 0.85f) {
        printf("ARC-20: Minting rejected. Coherence %.3f below threshold (0.85)\n", lambda_proof);
        return;
    }

    // Formula: Mint amount = 1000 * (lambda - 0.85) / 0.15
    uint64_t mint_amount = (uint64_t)(1000.0f * (lambda_proof - 0.85f) / 0.15f);
    token->total_supply += mint_amount;
    token->lambda_collateral = lambda_proof;

    printf("ARC-20: Minted %lu %s tokens based on coherence %.3f\n", mint_amount, token->symbol, lambda_proof);
}

void arc20_print_status(ARC20Token *token) {
    printf("ARC-20 Status [%s]: Supply: %lu, Coherence Collateral: %.3f\n",
           token->symbol, (uint64_t)token->total_supply, token->lambda_collateral);
}
