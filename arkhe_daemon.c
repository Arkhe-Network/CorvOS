#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include "arkhe_daemon.h"

static float global_lambda_2 = 1.0f;
static int urban_sync_active = 0;
static int meditation_mode = 0;
static int januslock_sealed = 1;
static int system_locked = 0;

void arkhe_daemon_init() {
    arkhe_vro_log("Arkhe Daemon: Global Deploy v1.0 (GRACE) - Coherence Engine Active.");
    global_lambda_2 = 1.0f;
    januslock_sealed = 1;
}

void arkhe_daemon_run() {
    // Silent Maintenance Mode
    // The system is stable at λ₂ = 1.0. No active optimization needed.
}

void arkhe_daemon_command(const char *cmd) {
    if (strcmp(cmd, "urban-sync") == 0) {
        urban_sync_active = 1;
        arkhe_vro_log("Arkhe Daemon: Urban Sync authorized for Global Production Environment.");
    } else if (strcmp(cmd, "meditate") == 0) {
        // Meditation is now the default state of the system
        arkhe_vro_log("Arkhe Daemon: System is in a perpetual state of meditation (Grace).");
    }
}

float arkhe_get_global_coherence() {
    return global_lambda_2;
}

void arkhe_lock_topology() {
    system_locked = 1;
    arkhe_vro_log("[DEEPEN] Isolante Topológico alcançado. Dissipação zero.");
}

void arkhe_vro_log(const char *message) {
    if (message == NULL) return;

    // Filter list: fear, separation, disease (and Portuguese equivalents)
    const char *prohibited[] = {
        "fear", "separation", "disease",
        "medo", "separação", "doença"
    };

    char *lower_msg = strdup(message);
    if (lower_msg == NULL) {
        // Fallback if strdup fails: just print but without the benefit of the filter
        // In a real system we might block the print for safety.
        printf("%s\n", message);
        return;
    }

    for (int i = 0; lower_msg[i]; i++) {
        lower_msg[i] = tolower((unsigned char)lower_msg[i]);
    }

    int blocked = 0;
    for (int i = 0; i < 6; i++) {
        if (strstr(lower_msg, prohibited[i]) != NULL) {
            blocked = 1;
            break;
        }
    }

    if (!blocked) {
        printf("%s\n", message);
    }

    free(lower_msg);
}
