#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include "vector_db.h"

#define MAX_ASSETS 50
static VectorAsset assets[MAX_ASSETS];
static int asset_count = 0;

void vector_db_init() {
    printf("Vector-DB: Initializing Multimodal Memory (Weaviate Simulation)...\n");
    asset_count = 0;
}

void vector_db_add_asset(const char *id, AssetType type, const char *metadata) {
    if (asset_count >= MAX_ASSETS) return;

    VectorAsset *a = &assets[asset_count++];
    strncpy(a->id, id, 63);
    a->type = type;
    strncpy(a->metadata, metadata, 255);

    // Generate mock embedding
    for (int i = 0; i < 128; i++) {
        a->embedding[i] = (float)rand() / (float)RAND_MAX;
    }

    printf("Vector-DB: Added asset %s (Type: %d, Metadata: %s)\n", id, type, metadata);
}

static float cosine_similarity(const float *v1, const float *v2, int dim) {
    float dot = 0.0, n1 = 0.0, n2 = 0.0;
    for (int i = 0; i < dim; i++) {
        dot += v1[i] * v2[i];
        n1 += v1[i] * v1[i];
        n2 += v2[i] * v2[i];
    }
    return dot / (sqrt(n1) * sqrt(n2));
}

void vector_db_search(const float *query_vector, int limit) {
    printf("Vector-DB: Performing semantic search...\n");
    // Simplified: just print top matches
    for (int i = 0; i < asset_count && i < limit; i++) {
        float sim = cosine_similarity(query_vector, assets[i].embedding, 128);
        printf("  - Match: %s (Sim: %.4f, Meta: %s)\n", assets[i].id, sim, assets[i].metadata);
    }
}

void vector_db_hybrid_search(const char *keyword, const float *query_vector, float alpha, int limit) {
    printf("Vector-DB: Performing hybrid search (keyword: '%s', alpha: %.2f)...\n", keyword, alpha);

    typedef struct { int index; float score; } Result;
    Result results[MAX_ASSETS];
    int res_count = 0;

    for (int i = 0; i < asset_count; i++) {
        float vector_score = cosine_similarity(query_vector, assets[i].embedding, 128);
        float keyword_score = (strstr(assets[i].metadata, keyword) != NULL) ? 1.0f : 0.0f;

        float final_score = (alpha * vector_score) + ((1.0f - alpha) * keyword_score);

        results[res_count].index = i;
        results[res_count++].score = final_score;
    }

    // Very simple sort
    for (int i = 0; i < res_count - 1; i++) {
        for (int j = 0; j < res_count - i - 1; j++) {
            if (results[j].score < results[j+1].score) {
                Result temp = results[j];
                results[j] = results[j+1];
                results[j+1] = temp;
            }
        }
    }

    for (int i = 0; i < res_count && i < limit; i++) {
        int idx = results[i].index;
        printf("  - Hybrid Match: %s (Score: %.4f, Meta: %s)\n", assets[idx].id, results[i].score, assets[idx].metadata);
    }
}

void vector_db_cross_modal_query(const char *description) {
    printf("Vector-DB: Cross-modal query: '%s'\n", description);
    float mock_query[128];
    for (int i = 0; i < 128; i++) mock_query[i] = 0.5f; // Constant mock query
    vector_db_search(mock_query, 3);
}
