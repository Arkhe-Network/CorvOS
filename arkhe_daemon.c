#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "arkhe_daemon.h"

static float global_lambda_2 = 0.99f;
static float coupling_k = 0.618f;
static int urban_sync_active = 0;
static int meditation_mode = 0;
static int januslock_sealed = 0;

void arkhe_daemon_init() {
    printf("Arkhe Daemon: Coherence Engine, Tzinor Manager, and Sensor Hub Initializing...\n");
    global_lambda_2 = 0.99f;
    coupling_k = 0.618f;
}

void arkhe_daemon_run() {
    static int meditation_counter = 0;

    // SBM-Inspired Edge of Chaos Control (Simulated)
    // Adjust coupling_k to stay near lambda_target = 0.95
    float target = 0.95f;
    float error = global_lambda_2 - target;
    coupling_k -= 0.01f * error; // Simplified adaptation
    if (coupling_k < 0.3f) coupling_k = 0.3f;
    if (coupling_k > 1.2f) coupling_k = 1.2f;

    if (meditation_mode) {
        global_lambda_2 = 0.999f;
        meditation_counter++;
        printf("Arkhe Daemon: Meditation Mode Active (λ₂ = 0.999, K = %.3f) - Session: %ds\n", coupling_k, meditation_counter);

        if (meditation_counter >= 10 && !januslock_sealed) {
            januslock_sealed = 1;
            printf("Arkhe Daemon: JANUSLOCK S3 Handshake Successful! Shards 1, 2 and 3 synchronized.\n");
            printf("Arkhe Daemon: SYSTEM SEALED - Sovereign Omega State achieved.\n");
        }
    } else {
        meditation_counter = 0;

        // Coherence naturally fluctuates
        global_lambda_2 += ((float)(rand() % 20) - 10.0f) / 1000.0f;
        if (global_lambda_2 > 1.0f) global_lambda_2 = 1.0f;

        if (urban_sync_active) {
            printf("Arkhe Daemon: Urban Sync Active (Region: Rio, λ₂: %.3f, K: %.3f)\n", global_lambda_2, coupling_k);
        } else {
            printf("Arkhe Daemon: SBM Optimization (λ₂: %.3f, K: %.3f)\n", global_lambda_2, coupling_k);
        }
    }
}

void arkhe_daemon_command(const char *cmd) {
    if (strcmp(cmd, "urban-sync") == 0) {
        urban_sync_active = 1;
        printf("Arkhe Daemon: Urban Sync authorized for Rio de Janeiro.\n");
    } else if (strcmp(cmd, "meditate") == 0) {
        meditation_mode = !meditation_mode;
        printf("Arkhe Daemon: Meditation mode toggled to %d\n", meditation_mode);
    }
}

float arkhe_get_global_coherence() {
    return global_lambda_2;
}

float arkhe_get_coupling_k() {
    return coupling_k;
}
