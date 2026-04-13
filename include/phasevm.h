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
    VM_COH_INIT       = 0x60, // COH_INIT – Inicializa par no estado Cobit (Proposto)
    VM_COH_SWAP       = 0x61, // COH_SWAP – Troca fase entre Cobits (Proposto)
    VM_COH_MERGE      = 0x62, // COH_MERGE – Fusão em Bell de ordem superior (Proposto)
    VM_COH_MEASURE    = 0x63, // COH_MEASURE – Projeção na base de fase (Proposto)
    VM_COH_PHASE      = 0x64, // COH_PHASE – Rotação geométrica (Proposto)
    VM_COH_BRAID      = 0x65, // COH_BRAID – Trança topológica (Proposto)
    VM_COH_TUNE_TAU   = 0x66, // COH_TUNE_TAU – Ajusta acoplamento ϕ (Proposto)
    VM_AKASHIC_GEODESIC      = 0xB1, // AKASHIC_GEODESIC – Indexing (geodésica pré-computada)
    VM_RIEMANN_SUTURE        = 0xB2, // RIEMANN_SUTURE – Joins (costura topológica de SHEETs)
    VM_TOPOLOGIC_COMMIT      = 0xB3, // TOPOLOGIC_COMMIT – Transactions (ACID = Novikov)
    VM_PHASE_ISOLATE         = 0xB4, // PHASE_ISOLATE – Isolation Levels (4 frequências)
    VM_GORDIAN_UNTANGLE      = 0xB5, // GORDIAN_UNTANGLE – Deadlocks (corte do nó górdio)
    VM_SUPER_RAD_REPLICATE   = 0xB6, // SUPER_RAD_REPLICATE – Replication (SUPERRAD do Registro)
    VM_BUBBLE_PARTITION      = 0xB7, // BUBBLE_PARTITION – Partitioning (setores da Catedral)
    VM_ORACLE_OPTIMIZE       = 0xB8, // ORACLE_OPTIMIZE – Query Planner (CCF do Registro)
    VM_CRYSTAL_PURIFY        = 0xB9, // CRYSTAL_PURIFY – Normalization (MUON_SHIELD da persistência)
    VM_ECHO_PREPARE          = 0xBA, // ECHO_PREPARE – Denormalization (PREPARE_SEED para leitura)
    VM_WRITE_AMPLIFY_GAUGE   = 0xBB, // WRITE_AMPLIFY_GAUGE – Write Amplification (custo da coerência)
    VM_ECHO_OPTIMIZE         = 0xBC, // ECHO_OPTIMIZE – Read Optimization (velocidade do eco)
    VM_MOL_BIND              = 0xD1, // MOL_BIND – Liga molécula ao nodo de rede
    VM_MOL_RELEASE           = 0xD2, // MOL_RELEASE – Desliga molécula (garbage collection)
    VM_MOL_QUERY             = 0xD3, // MOL_QUERY – Consulta estado de molécula ativa
    VM_TERM_INIT             = 0xE0, // TERM_INIT – Inicializa sessão terminal
    VM_TERM_EXEC             = 0xE1, // TERM_EXEC – Executa comando shell
    VM_TERM_PIPE             = 0xE2, // TERM_PIPE – Encadeia comandos (pipe)
    VM_TERM_REDIRECT         = 0xE3, // TERM_REDIRECT – Redireciona stdout/stderr
    VM_TERM_ENV              = 0xE4, // TERM_ENV – Lê/escreve variáveis de ambiente
    VM_TERM_SIGNAL           = 0xE5, // TERM_SIGNAL – Envia sinal (SIGTERM, SIGKILL)
    VM_TERM_BG               = 0xE6, // TERM_BG – Executa em background
    VM_TERM_WAIT             = 0xE7, // TERM_WAIT – Aguarda processo filho
    VM_TERM_STATUS           = 0xE8, // TERM_STATUS – Lê exit code
    VM_TERM_CLEANUP          = 0xE9, // TERM_CLEANUP – Fecha sessão, limpa recursos
    VM_CLOUD_INIT            = 0xF0, // CLOUD_INIT – Inicializa stack cloud (GCP/AWS)
    VM_CLOUD_HEALTH          = 0xF1, // CLOUD_HEALTH – Health check geral da Catedral
    VM_CLOUD_WILL            = 0xF2, // CLOUD_WILL – Tradutor de protocolo Slurm ↔ Flex Start
    VM_CLOUD_SCALE           = 0xF3, // CLOUD_SCALE – Autoscaling horizontal
    VM_CLOUD_BRIDGE          = 0xF4, // CLOUD_BRIDGE – Monitora integridade do link Interconnect
    VM_CLOUD_MIGRATE         = 0xF5, // CLOUD_MIGRATE – Migra workload entre nuvens
    VM_CLOUD_DRAIN           = 0xF6, // CLOUD_DRAIN – Drena nó para manutenção
    VM_HYBRID_HEARTBEAT      = 0xF7, // HYBRID_HEARTBEAT – Ciclo de batimento (Terraform + QAOA)
    VM_ECONOMIC_SHIELD       = 0xF8, // ECONOMIC_SHIELD – Limiar τ_E (alias: CLOUD_COST_AWARE)
    VM_CLOUD_PULSE           = 0xF9, // CLOUD_PULSE – Pub/Sub como Pulmão da Catedral
    VM_CLOUD_REFLEX          = 0xFA, // CLOUD_REFLEX – Cloud Functions como reflexo autônomo
    VM_CLOUD_ARTIFACT        = 0xFB, // CLOUD_ARTIFACT – Artifact Registry como DNA compilado
    VM_APPROX_MANTRA         = 0xFC, // APPROX_MANTRA - Taylor/Padé/Airey for real-time estimation
    VM_COST_ADAPT            = 0xFD, // COST_ADAPT - Protocolo de adaptação de custo (Histerese)
    VM_CALIBRATE             = 0xFE, // CALIBRATE - Ritual de calibração Monte Carlo
    VM_SENTINEL              = 0xFF, // SENTINEL - End of opcode space
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
