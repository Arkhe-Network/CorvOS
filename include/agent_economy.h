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
typedef struct {
    float semantic;
    float punctuality;
    float honesty;
    float originality;
    float satisfaction;
} ReputationVector;

float oracle_calculate_novelty(const float *result_vector, int dim);
ReputationVector oracle_evaluate_multifactor(const char *agent_id, const float *intent_v, const float *result_v, int dim);
void oracle_update_reputation_ewma(const char *agent_id, ReputationVector new_metrics);

// Cascade Monetization (Multi-level Royalty Tree)
typedef struct {
    char node_id[64];
    char parent_id[64];
    char contributor[64];
    uint32_t royalty_bp; // Basis points (100 = 1%)
} ContributionNode;

void contract_register_node(const char *id, const char *parent, const char *contributor, uint32_t bp);
void contract_recursive_distribute(const char *leaf_id, uint64_t amount);

#endif
