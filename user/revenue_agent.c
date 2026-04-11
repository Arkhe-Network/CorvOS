#include <stdio.h>
#include <unistd.h>
#include "../include/revenue_mesh.h"
#include "../include/arkhe_daemon.h"
#include "../include/self_healing.h"
#include "../include/vector_db.h"

void revenue_agent_run() {
    printf("Revenue-Agent: Initializing Revenue Mesh & Horizon 2 Services...\n");
    revenue_mesh_init();
    self_healing_init();
    vector_db_init();

    // Populate Vector DB
    vector_db_add_asset("img_01", ASSET_IMAGE, "Stock market crash 1987");
    vector_db_add_asset("txt_01", ASSET_TEXT, "Inflation analysis H1 2026");

    const char *test_users[] = {"user_01", "user_02", "user_new"};
    int num_users = 3;

    for (int cycle = 0; cycle < 2; cycle++) {
        printf("\n--- Revenue Cycle %d ---\n", cycle + 1);

        for (int i = 0; i < num_users; i++) {
            const char *uid = test_users[i];

            // Simulate user activity
            revenue_process_event(uid, "article_view");

            // Get monetization decision
            RevenueDecision decision = revenue_decide_strategy(uid);

            printf("Revenue-Agent: User %s -> Strategy: %s, Message: '%s', Value: $%.4f\n",
                   uid, revenue_strategy_to_string(decision.strategy), decision.display_text, decision.price);

            if (decision.strategy == MONETIZATION_SUBSCRIPTION) {
                printf("Revenue-Agent: User %s triggered subscription offer. Simulating purchase...\n", uid);
                revenue_process_event(uid, "subscription_purchased");
            }

            // Report metrics to Self-Healing
            self_healing_report_latency("Revenue-Mesh", 15.0f);
        }

        // Multimodal Search Simulation
        if (cycle == 0) {
            vector_db_cross_modal_query("Economic crisis history");
        }

        // Chaos Engineering Simulation (Gremlin)
        if (cycle == 0) {
            printf("\n--- Gremlin Chaos Experiment: Critical Failures on Ad-Server ---\n");
            for (int e = 0; e < 6; e++) {
                self_healing_report_latency("Ad-Server", 800.0f); // Should trigger remediation after 6 calls
            }
        }

        // Toggle meditation to see impact of high coherence
        if (cycle == 0) {
            printf("\nRevenue-Agent: Triggering system meditation for maximum coherence...\n");
            arkhe_daemon_command("meditate");
            sleep(1);
        }
    }

    printf("\nRevenue-Agent: Operation cycle finished.\n");
}
