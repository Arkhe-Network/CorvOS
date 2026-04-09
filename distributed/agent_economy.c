#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "arkhe_chain.h"
#include "arc20.h"
#include "agent_economy.h"

void agent_send_message(const char *sender, const char *receiver, const char *content, float lambda) {
    printf("φ-MSG: [%s] -> [%s]: '%s' (Req λ: %.2f)\n", sender, receiver, content, lambda);
    // Blockchain logging
    char block_data[512];
    snprintf(block_data, 512, "MSG: %s->%s: %s", sender, receiver, content);
    arkhe_chain_add_block(block_data);
}

void contract_split_revenue(uint64_t amount, RevenueStakeholder *stakeholders, int count) {
    printf("ARC-Contract: Splitting %lu tokens among %d agents...\n", (unsigned long)amount, count);
    for (int i = 0; i < count; i++) {
        uint64_t share = (amount * stakeholders[i].shares) / 100;
        printf("  - Agent %s received %lu tokens (%d%%)\n", stakeholders[i].agent_id, (unsigned long)share, stakeholders[i].shares);
    }
}

// Vector Reputation Oracle implementation
static float cosine_sim(const float *v1, const float *v2, int dim) {
    float dot = 0.0, n1 = 0.0, n2 = 0.0;
    for (int i = 0; i < dim; i++) {
        dot += v1[i] * v2[i];
        n1 += v1[i] * v1[i];
        n2 += v2[i] * v2[i];
    }
    float den = sqrt(n1) * sqrt(n2);
    return (den == 0) ? 0 : dot / den;
}

float oracle_calculate_novelty(const float *result_vector, int dim) {
    // In a real impl, this would query Weaviate. Here we simulate it.
    (void)result_vector; (void)dim;
    float novelty = 0.85f + ((float)rand() / (float)RAND_MAX) * 0.15f;
    printf("Oracle: Novelty Index calculated: %.4f\n", novelty);
    return novelty;
}

ReputationVector oracle_evaluate_multifactor(const char *agent_id, const float *intent_v, const float *result_v, int dim) {
    ReputationVector v;
    v.semantic = cosine_sim(intent_v, result_v, dim);
    v.punctuality = 0.95f; // Mock: always on time
    v.honesty = 1.0f;     // Mock: no disputes
    v.originality = oracle_calculate_novelty(result_v, dim);
    v.satisfaction = 0.90f; // Mock: good feedback

    printf("Oracle: Multifactor Evaluation for %s [Sem: %.2f, Orig: %.2f]\n", agent_id, v.semantic, v.originality);
    return v;
}

void oracle_update_reputation_ewma(const char *agent_id, ReputationVector new_metrics) {
    float gamma = 0.8f;
    // Mocking historical state update
    float aggregate = (new_metrics.semantic + new_metrics.punctuality + new_metrics.honesty +
                      new_metrics.originality + new_metrics.satisfaction) / 5.0f;

    printf("Oracle: EWMA Update for %s - New Aggregate Score: %.4f (Gamma: %.1f)\n", agent_id, aggregate * gamma, gamma);
}

// Cascade Monetization implementation (Recursive Royalty Tree)
#define MAX_NODES 100
static ContributionNode royalty_tree[MAX_NODES];
static int node_count = 0;

void contract_register_node(const char *id, const char *parent, const char *contributor, uint32_t bp) {
    if (node_count >= MAX_NODES) return;
    ContributionNode *n = &royalty_tree[node_count++];
    strncpy(n->node_id, id, 63);
    strncpy(n->parent_id, parent, 63);
    strncpy(n->contributor, contributor, 63);
    n->royalty_bp = bp;
    printf("ARC-Contract: Registered Node %s (Parent: %s, Contributor: %s, Royalty: %u bp)\n", id, parent, contributor, bp);
}

void contract_recursive_distribute(const char *leaf_id, uint64_t amount) {
    printf("ARC-Contract: Initiating Recursive Distribution from leaf %s (Total: %lu ASI)\n", leaf_id, (unsigned long)amount);
    char current_id[64];
    strncpy(current_id, leaf_id, 63);
    uint64_t remaining = amount;
    int depth = 0;

    while (strcmp(current_id, "0x0") != 0 && depth < 10) {
        depth++;
        int found = 0;
        for (int i = 0; i < node_count; i++) {
            if (strcmp(royalty_tree[i].node_id, current_id) == 0) {
                // Overflow check: amount * bp / 10000
                if (amount > 0 && royalty_tree[i].royalty_bp > 0xFFFFFFFFFFFFFFFFULL / amount) {
                    printf("  [ERROR] Math overflow in royalty calculation!\n");
                    return;
                }
                uint64_t share = (amount * royalty_tree[i].royalty_bp) / 10000;
                printf("  -> Paid %lu ASI to %s (Node: %s)\n", (unsigned long)share, royalty_tree[i].contributor, current_id);
                remaining -= share;
                strncpy(current_id, royalty_tree[i].parent_id, 63);
                found = 1;
                break;
            }
        }
        if (!found) break;
    }
    if (depth >= 10) printf("  [WARNING] Max tree depth reached during distribution.\n");
    printf("  -> Remaining %lu ASI sent to ASI Foundation Treasury.\n", (unsigned long)remaining);
}
