#ifndef REVENUE_MESH_H
#define REVENUE_MESH_H

#include <stdint.h>

typedef enum {
    MONETIZATION_NONE,
    MONETIZATION_AD,
    MONETIZATION_SUBSCRIPTION,
    MONETIZATION_PREMIUM_EXP
} MonetizationStrategy;

typedef struct {
    char user_id[64];
    float ltv_estimated;
    float churn_risk;
    int articles_read_this_month;
    char segment[32]; // e.g., "tech_enthusiast", "casual_reader"
} UserProfile;

typedef struct {
    MonetizationStrategy strategy;
    char offer_id[64];
    char display_text[256];
    float price;
} RevenueDecision;

typedef struct {
    char ad_unit_id[64];
    float min_cpm;
} AdOffer;

typedef enum {
    PAYWALL_DISABLED,
    PAYWALL_SOFT,
    PAYWALL_HARD,
    PAYWALL_DYNAMIC
} PaywallType;

typedef struct {
    PaywallType type;
    int limit;
} PaywallConfig;

// Revenue Mesh Services
void revenue_mesh_init();
UserProfile revenue_get_user_profile(const char *user_id);
RevenueDecision revenue_decide_strategy(const char *user_id);
void revenue_process_event(const char *user_id, const char *event_type);
const char* revenue_strategy_to_string(MonetizationStrategy strategy);

// Internal Mock Services
AdOffer revenue_ad_auction(const char *user_id);
PaywallConfig revenue_get_paywall_config(const char *user_id);

#endif
