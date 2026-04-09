#ifndef VECTOR_DB_H
#define VECTOR_DB_H

#include <stdint.h>

typedef enum {
    ASSET_TEXT,
    ASSET_IMAGE,
    ASSET_AUDIO,
    ASSET_VIDEO
} AssetType;

typedef struct {
    char id[64];
    AssetType type;
    float embedding[128]; // Simplified 128-dim vector
    char metadata[256];
} VectorAsset;

void vector_db_init();
void vector_db_add_asset(const char *id, AssetType type, const char *metadata);
void vector_db_search(const float *query_vector, int limit);
void vector_db_hybrid_search(const char *keyword, const float *query_vector, float alpha, int limit);
void vector_db_cross_modal_query(const char *description);

#endif
