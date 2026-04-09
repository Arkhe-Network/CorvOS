#ifndef AGENT_ECONOMY_H
#define AGENT_ECONOMY_H

#include <stdint.h>

// Communication Protocol: Coherent Message (φ-MSG)
typedef struct {
    char sender[64];
    char receiver[64];
    char content[256];
    float lambda_required;
} CoherentMessage;

void agent_send_message(const char *sender, const char *receiver, const char *content, float lambda);

// ARC-20 Smart Contract: Revenue Split
typedef struct {
    char agent_id[64];
    uint32_t shares; // parts per 100
} RevenueStakeholder;

void contract_split_revenue(uint64_t amount, RevenueStakeholder *stakeholders, int count);

// Vector Reputation Oracle
float oracle_evaluate_result(const float *intent_vector, const float *result_vector, int dim);
void oracle_update_reputation(const char *agent_id, float coherence_score);

// Cascade Monetization
void contract_cascade_distribute(uint64_t total_revenue, const char *article_id);

#endif
