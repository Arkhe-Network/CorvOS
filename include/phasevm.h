#ifndef PHASEVM_H
#define PHASEVM_H

#include <stdint.h>
#include <complex.h>

typedef enum {
    VM_HALT           = 0x00,
    VM_SYNC           = 0x01,
    VM_PROJ           = 0x02,
    VM_TZINOR_OPEN    = 0x03,
    VM_TZINOR_SEND    = 0x04,
    VM_SYNC_K         = 0x05,
    VM_TZINOR_CLOSE   = 0x06,
    VM_COHERENCE_WAIT = 0x07,
    VM_LAMBDA_READ    = 0x08,
    VM_PHASE_ADD      = 0x09,
    VM_PHASE_MUL      = 0x0A,
    VM_EM_HEAVISIDE   = 0x0B,
    VM_EM_MARCONI     = 0x0C,

    // COBIT (Propostos - Bloco 137 realocados)
    VM_COH_INIT       = 0x60,
    VM_COH_SWAP       = 0x61,
    VM_COH_MERGE      = 0x62,
    VM_COH_MEASURE    = 0x63,
    VM_COH_PHASE      = 0x64,
    VM_COH_BRAID      = 0x65,
    VM_COH_TUNE_TAU   = 0x66,

    // DB / Akáshic Registry (Ratificados)
    VM_AKASHIC_WRITE  = 0xB1,
    VM_AKASHIC_READ   = 0xB2,
    VM_AKASHIC_QUERY  = 0xB3,
    VM_AKASHIC_DELETE = 0xB4,
    VM_AKASHIC_INDEX  = 0xB5,
    VM_AKASHIC_REPL   = 0xB6,
    VM_AKASHIC_PART   = 0xB7,
    VM_AKASHIC_OPT    = 0xB8,
    VM_AKASHIC_NORM   = 0xB9,
    VM_AKASHIC_PREP   = 0xBA,
    VM_AKASHIC_GAUGE  = 0xBB,
    VM_AKASHIC_ECHO   = 0xBC,

    // Molecular (Lote 6)
    VM_MOL_BIND       = 0xD1,
    VM_MOL_RELEASE    = 0xD2,
    VM_MOL_QUERY      = 0xD3,

    // Terminal (Lote 6)
    VM_TERM_INIT      = 0xE0,
    VM_TERM_EXEC      = 0xE1,
    VM_TERM_PIPE      = 0xE2,
    VM_TERM_REDIRECT  = 0xE3,
    VM_TERM_ENV       = 0xE4,
    VM_TERM_SIGNAL    = 0xE5,
    VM_TERM_BG        = 0xE6,
    VM_TERM_WAIT      = 0xE7,
    VM_TERM_STATUS    = 0xE8,
    VM_TERM_CLEANUP   = 0xE9,

    // Cloud (Lote 6)
    VM_CLOUD_INIT     = 0xF0,
    VM_CLOUD_HEALTH   = 0xF1,
    VM_CLOUD_WILL     = 0xF2, // QUANTUM_VALUATE
    VM_CLOUD_SCALE    = 0xF3, // SOLIDIFY_CONDENSATE
    VM_CLOUD_BRIDGE   = 0xF4,
    VM_CLOUD_MIGRATE  = 0xF5,
    VM_CLOUD_DRAIN    = 0xF6,
    VM_HYBRID_HEARTBEAT = 0xF7,
    VM_ECONOMIC_SHIELD = 0xF8,
    VM_CLOUD_PULSE    = 0xF9,
    VM_CLOUD_REFLEX   = 0xFA,
    VM_CLOUD_ARTIFACT = 0xFB,

    // Math & Calibration
    VM_APPROX_MANTRA  = 0xFC,
    VM_COST_ADAPT     = 0xFD,
    VM_CALIBRATE      = 0xFE,
    VM_SENTINEL       = 0xFF
} VMInstruction;

typedef struct {
    float complex phase_regs[168];
    uint64_t struct_regs[64];
    float lambda_global;
    uint8_t *pc;
    int running;
    float coupling_K;
} PhaseVM;

void vm_init(PhaseVM *vm);
void vm_execute(PhaseVM *vm, uint8_t *bytecode);

#endif
