#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "self_healing.h"
#include "arkhe_daemon.h"

#define MAX_COMPONENTS 10
static ComponentHealth components[MAX_COMPONENTS];
static int component_count = 0;

void self_healing_init() {
    printf("Self-Healing: Initializing Immune System...\n");
    component_count = 0;

    // Register core components
    strcpy(components[component_count].component_name, "Revenue-Mesh");
    components[component_count].status = HEALTH_OK;
    components[component_count].latency_ms = 10.0f;
    components[component_count].error_count = 0;
    component_count++;

    strcpy(components[component_count].component_name, "Ad-Server");
    components[component_count].status = HEALTH_OK;
    components[component_count].latency_ms = 45.0f;
    components[component_count].error_count = 0;
    component_count++;

    strcpy(components[component_count].component_name, "Vector-DB");
    components[component_count].status = HEALTH_OK;
    components[component_count].latency_ms = 25.0f;
    components[component_count].error_count = 0;
    component_count++;
}

void self_healing_report_error(const char *component) {
    for (int i = 0; i < component_count; i++) {
        if (strcmp(components[i].component_name, component) == 0) {
            components[i].error_count++;
            if (components[i].error_count > 5) {
                components[i].status = HEALTH_CRITICAL;
                printf("Self-Healing: Component %s is CRITICAL!\n", component);
                self_healing_remediate(component);
            } else if (components[i].error_count > 2) {
                components[i].status = HEALTH_DEGRADED;
                printf("Self-Healing: Component %s is DEGRADED.\n", component);
            }
            return;
        }
    }
}

void self_healing_report_latency(const char *component, float ms) {
    for (int i = 0; i < component_count; i++) {
        if (strcmp(components[i].component_name, component) == 0) {
            components[i].latency_ms = ms;
            if (ms > 500.0f) {
                printf("Self-Healing: High latency detected in %s (%.1fms)\n", component, ms);
                self_healing_report_error(component);
            }
            return;
        }
    }
}

void self_healing_remediate(const char *component) {
    printf("Self-Healing: Initiating remediation for %s...\n", component);

    // Simulate remediation steps
    if (strcmp(component, "Ad-Server") == 0) {
        printf("Self-Healing: Restarting Ad-Server pods and clearing edge cache.\n");
    } else if (strcmp(component, "Revenue-Mesh") == 0) {
        printf("Self-Healing: Scaling Revenue-Mesh nodes and activating circuit breakers.\n");
    }

    // Reset status after "remediation"
    for (int i = 0; i < component_count; i++) {
        if (strcmp(components[i].component_name, component) == 0) {
            components[i].status = HEALTH_OK;
            components[i].error_count = 0;
            components[i].latency_ms = 10.0f;
            printf("Self-Healing: Component %s RESTORED to HEALTH_OK.\n", component);
            return;
        }
    }
}

void self_healing_monitor() {
    float lambda = arkhe_get_global_coherence();
    if (lambda < 0.80f) {
        printf("Self-Healing: Low global coherence (λ₂: %.3f). Hardening all circuits.\n", lambda);
    }
}

HealthStatus self_healing_get_status(const char *component) {
    for (int i = 0; i < component_count; i++) {
        if (strcmp(components[i].component_name, component) == 0) {
            return components[i].status;
        }
    }
    return HEALTH_OK;
}
