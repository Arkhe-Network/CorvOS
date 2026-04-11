#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "revenue_mesh.h"
#include "arkhe_daemon.h"

#define MAX_PROFILES 100

// Mock database for User Profiles
static UserProfile mock_profiles[MAX_PROFILES];
static int profile_count = 0;

static void safe_strcpy(char *dest, const char *src, size_t size) {
    strncpy(dest, src, size - 1);
    dest[size - 1] = '\0';
}

void revenue_mesh_init() {
    printf("Revenue Mesh: Initializing Revenue Services...\n");
    profile_count = 0;

    // Initialize some mock users
    UserProfile *p1 = &mock_profiles[profile_count++];
    safe_strcpy(p1->user_id, "user_01", sizeof(p1->user_id));
    p1->ltv_estimated = 150.0f;
    p1->churn_risk = 0.1f;
    p1->articles_read_this_month = 5;
    safe_strcpy(p1->segment, "tech_enthusiast", sizeof(p1->segment));

    UserProfile *p2 = &mock_profiles[profile_count++];
    safe_strcpy(p2->user_id, "user_02", sizeof(p2->user_id));
    p2->ltv_estimated = 20.0f;
    p2->churn_risk = 0.6f;
    p2->articles_read_this_month = 12;
    safe_strcpy(p2->segment, "casual_reader", sizeof(p2->segment));
}

UserProfile revenue_get_user_profile(const char *user_id) {
    for (int i = 0; i < profile_count; i++) {
        if (strcmp(mock_profiles[i].user_id, user_id) == 0) {
            return mock_profiles[i];
        }
    }

    // Default profile for new/unknown users
    UserProfile default_p = {0};
    safe_strcpy(default_p.user_id, user_id, sizeof(default_p.user_id));
    default_p.ltv_estimated = 0.0f;
    default_p.churn_risk = 0.5f;
    default_p.articles_read_this_month = 0;
    safe_strcpy(default_p.segment, "unknown", sizeof(default_p.segment));
    return default_p;
}

void revenue_process_event(const char *user_id, const char *event_type) {
    printf("Revenue Mesh: Processing event '%s' for user '%s'\n", event_type, user_id);
    int index = -1;
    for (int i = 0; i < profile_count; i++) {
        if (strcmp(mock_profiles[i].user_id, user_id) == 0) {
            index = i;
            break;
        }
    }

    if (index == -1) {
        if (profile_count < MAX_PROFILES) {
            index = profile_count++;
            UserProfile *np = &mock_profiles[index];
            safe_strcpy(np->user_id, user_id, sizeof(np->user_id));
            np->ltv_estimated = 0.0f;
            np->churn_risk = 0.5f;
            np->articles_read_this_month = 0;
            safe_strcpy(np->segment, "new_user", sizeof(np->segment));
            printf("Revenue Mesh: Created new profile for %s\n", user_id);
        } else {
            printf("Revenue Mesh: Profile database full, event ignored for %s\n", user_id);
            return;
        }
    }

    UserProfile *p = &mock_profiles[index];
    if (strcmp(event_type, "article_view") == 0) {
        p->articles_read_this_month++;
        p->ltv_estimated += 0.5f;
    } else if (strcmp(event_type, "subscription_purchased") == 0) {
        p->ltv_estimated += 100.0f;
        p->churn_risk = 0.01f;
        safe_strcpy(p->segment, "premium_subscriber", sizeof(p->segment));
    }
}

AdOffer revenue_ad_auction(const char *user_id) {
    AdOffer offer;
    safe_strcpy(offer.ad_unit_id, "top_banner_01", sizeof(offer.ad_unit_id));

    UserProfile p = revenue_get_user_profile(user_id);
    offer.min_cpm = 5.0f + (p.ltv_estimated * 0.05f);

    printf("Revenue Mesh: Ad Auction for %s - Selected Unit: %s (CPM: $%.2f)\n",
           user_id, offer.ad_unit_id, offer.min_cpm);
    return offer;
}

PaywallConfig revenue_get_paywall_config(const char *user_id) {
    PaywallConfig config;
    UserProfile p = revenue_get_user_profile(user_id);

    if (strcmp(p.segment, "premium_subscriber") == 0) {
        config.type = PAYWALL_DISABLED;
        config.limit = -1;
    } else if (p.articles_read_this_month > 10) {
        config.type = PAYWALL_HARD;
        config.limit = 10;
    } else {
        config.type = PAYWALL_SOFT;
        config.limit = 10;
    }

    return config;
}

RevenueDecision revenue_decide_strategy(const char *user_id) {
    RevenueDecision decision;
    safe_strcpy(decision.offer_id, "default_offer", sizeof(decision.offer_id));

    UserProfile p = revenue_get_user_profile(user_id);
    PaywallConfig pw = revenue_get_paywall_config(user_id);
    float lambda = arkhe_get_global_coherence();

    printf("Revenue Mesh: Decision Engine for %s (λ₂: %.3f)\n", user_id, lambda);

    if (lambda < 0.70f) {
        decision.strategy = MONETIZATION_NONE;
        safe_strcpy(decision.display_text, "Enjoy a clean experience for better coherence.", sizeof(decision.display_text));
        decision.price = 0.0f;
    } else if (pw.type == PAYWALL_HARD) {
        decision.strategy = MONETIZATION_SUBSCRIPTION;
        safe_strcpy(decision.display_text, "Join ASI Premium for unlimited access!", sizeof(decision.display_text));
        decision.price = 9.99f;
        safe_strcpy(decision.offer_id, "premium_sub_2026", sizeof(decision.offer_id));
    } else if (p.churn_risk > 0.5f && lambda > 0.90f) {
        decision.strategy = MONETIZATION_PREMIUM_EXP;
        safe_strcpy(decision.display_text, "Special Invitation: Arkhe-Block Exclusive Lounge", sizeof(decision.display_text));
        decision.price = 0.0f;
    } else {
        decision.strategy = MONETIZATION_AD;
        AdOffer ad = revenue_ad_auction(user_id);
        snprintf(decision.display_text, sizeof(decision.display_text), "Sponsored: %s", ad.ad_unit_id);
        decision.price = ad.min_cpm / 1000.0f;
    }

    return decision;
}

const char* revenue_strategy_to_string(MonetizationStrategy strategy) {
    switch (strategy) {
        case MONETIZATION_NONE: return "NONE";
        case MONETIZATION_AD: return "AD";
        case MONETIZATION_SUBSCRIPTION: return "SUBSCRIPTION";
        case MONETIZATION_PREMIUM_EXP: return "PREMIUM_EXP";
        default: return "UNKNOWN";
    }
}
