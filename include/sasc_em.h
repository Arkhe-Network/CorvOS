#ifndef SASC_EM_H
#define SASC_EM_H

#include <stdint.h>

typedef struct {
    float e_field_strength;
    float h_field_strength;
    float em_lambda2;
    uint32_t frequency_hz;
} SASC_EM_State;

void sasc_em_init();
void sasc_em_update(uint32_t freq, float e, float h);
float sasc_em_get_coherence();
void sasc_em_report();

#endif
