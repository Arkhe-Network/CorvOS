#ifndef PHASEVM_H
#define PHASEVM_H

#include <stdint.h>
#include <complex.h>

// ISA-φ v1.0 Instruction Set
typedef enum {
    VM_SYNC           = 0x01, // SYNC – sincroniza a fase local com a rede Tzinor
    VM_PROJ           = 0x02, // PROJ – projecta o estado de fase em estrutura (colapso C→Z)
    VM_TZINOR_OPEN    = 0x03, // TZINOR_OPEN – abre um canal retrocausal
    VM_TZINOR_SEND    = 0x04, // TZINOR_SEND – envia um pacote de fase
    VM_SYNC_K         = 0x05, // SYNC_K – ajusta o parâmetro de acoplamento
    VM_TZINOR_CLOSE   = 0x06, // TZINOR_CLOSE – fecha um canal retrocausal
    VM_COHERENCE_WAIT = 0x07, // COHERENCE_WAIT – aguarda até λ₂ atingir o limite
    VM_LAMBDA_READ    = 0x08, // LAMBDA_READ – lê o valor atual de λ₂
    VM_PHASE_ADD      = 0x09, // PHASE_ADD – adição complexa de fases
    VM_PHASE_MUL      = 0x0A, // PHASE_MUL – multiplicação complexa de fases
    VM_EM_HEAVISIDE   = 0x0B, // EM_HEAVISIDE – Forward EM prediction (Characterization)
    VM_EM_MARCONI     = 0x0C, // EM_MARCONI – Inverse EM design (Synthesis)
    VM_HALT           = 0x00
} VMInstruction;

typedef struct {
    float complex phase_regs[168]; // 168 registers for NV centers
    uint64_t struct_regs[64];
    float lambda_global;
    uint8_t *pc;
    int running;
    float coupling_K;
} PhaseVM;

void vm_init(PhaseVM *vm);
void vm_execute(PhaseVM *vm, uint8_t *bytecode);

#endif
