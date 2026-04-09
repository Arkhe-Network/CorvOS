#ifndef SELF_HEALING_H
#define SELF_HEALING_H

#include <stdint.h>

typedef enum {
    HEALTH_OK,
    HEALTH_DEGRADED,
    HEALTH_CRITICAL
} HealthStatus;

typedef struct {
    char component_name[64];
    HealthStatus status;
    float latency_ms;
    int error_count;
} ComponentHealth;

void self_healing_init();
void self_healing_monitor();
void self_healing_report_error(const char *component);
void self_healing_report_latency(const char *component, float ms);
HealthStatus self_healing_get_status(const char *component);

// Remediação
void self_healing_remediate(const char *component);

#endif
