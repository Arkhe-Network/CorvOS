#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "arkhe_chain.h"
#include "arc20.h"

// Communication Protocol: Coherent Message (φ-MSG)
typedef struct {
    char sender[64];
    char receiver[64];
    char content[256];
    float lambda_required;
} CoherentMessage;

void agent_send_message(const char *sender, const char *receiver, const char *content, float lambda) {
    printf("φ-MSG: [%s] -> [%s]: '%s' (Req λ: %.2f)\n", sender, receiver, content, lambda);
    // Blockchain logging
    char block_data[512];
    snprintf(block_data, 512, "MSG: %s->%s: %s", sender, receiver, content);
    arkhe_chain_add_block(block_data);
}

// ARC-20 Smart Contract: Revenue Split
typedef struct {
    char agent_id[64];
    uint32_t shares; // parts per 100
} RevenueStakeholder;

void contract_split_revenue(uint64_t amount, RevenueStakeholder *stakeholders, int count) {
    printf("ARC-Contract: Splitting %lu tokens among %d agents...\n", amount, count);
    for (int i = 0; i < count; i++) {
        uint64_t share = (amount * stakeholders[i].shares) / 100;
        printf("  - Agent %s received %lu tokens (%d%%)\n", stakeholders[i].agent_id, share, stakeholders[i].shares);
    }
}

// Vector Reputation Oracle implementation
#include <math.h>

static float cosine_sim(const float *v1, const float *v2, int dim) {
    float dot = 0.0, n1 = 0.0, n2 = 0.0;
    for (int i = 0; i < dim; i++) {
        dot += v1[i] * v2[i];
        n1 += v1[i] * v1[i];
        n2 += v2[i] * v2[i];
    }
    return dot / (sqrt(n1) * sqrt(n2));
}

float oracle_evaluate_result(const float *intent_vector, const float *result_vector, int dim) {
    float score = cosine_sim(intent_vector, result_vector, dim);
    printf("Oracle: Evaluating agent result coherence... Score: %.4f\n", score);
    return score;
}

void oracle_update_reputation(const char *agent_id, float coherence_score) {
    printf("Oracle: Updating reputation for agent %s based on coherence %.4f\n", agent_id, coherence_score);
    if (coherence_score < 0.70f) {
        printf("Oracle: [SLASHING] Agent %s reputation penalized for low coherence!\n", agent_id);
    }
}

// Cascade Monetization implementation
void contract_cascade_distribute(uint64_t total_revenue, const char *article_id) {
    printf("ARC-Contract: Cascade Monetization for Article %s (Total: %lu ASI)\n", article_id, total_revenue);

    // Static cascade rule: 40% Human Author, 30% Research Agent, 20% Synthesis Agent, 10% Foundation
    uint64_t author_share = (total_revenue * 40) / 100;
    uint64_t research_share = (total_revenue * 30) / 100;
    uint64_t synthesis_share = (total_revenue * 20) / 100;
    uint64_t foundation_share = total_revenue - (author_share + research_share + synthesis_share);

    printf("  - [Human] Author: %lu ASI\n", author_share);
    printf("  - [Agent] Research-01: %lu ASI\n", research_share);
    printf("  - [Agent] Synthesis-01: %lu ASI\n", synthesis_share);
    printf("  - [Protocol] Foundation Treasury: %lu ASI\n", foundation_share);
}
