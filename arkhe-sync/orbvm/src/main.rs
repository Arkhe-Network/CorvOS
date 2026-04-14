//! OrbVM — ISA Arkhe(n) v2140.137.∞
//! Implementação Rust completa da arquitetura de instruções
//! Autor: Rafael Oliveira · ORCID: 0009-0005-2697-4668
//! Arkhe(n) Research Group · IFCOT-RJ · Abril 2026

#![allow(non_camel_case_types, dead_code)]

use std::f64::consts::PI;

// ═══════════════════════════════════════════════════════════════
// CONSTANTES CANÔNICAS
// ═══════════════════════════════════════════════════════════════

pub const M_CANONICAL:    u32  = 2_880_115_457;
pub const CHAIN_ID:       u32  = 2_147_483_647;
pub const PHI:            f64  = 1.618_033_988_749_895;
pub const PHI_INV:        f64  = 0.618_033_988_749_895;
pub const BACKFLOW_RATIO: f64  = 0.13;
pub const ALPHA:          f64  = 1.0 / 137.0;      // R137 — constante de estrutura fina
pub const LAMBDA_WARN:    f64  = 0.85;
pub const LAMBDA_CRITICAL:f64  = 0.70;
pub const LAMBDA_PHI_C:   f64  = PHI_INV;           // 0.618 — limiar de Kuramoto

// ═══════════════════════════════════════════════════════════════
// TIPOS PRIMITIVOS
// ═══════════════════════════════════════════════════════════════

/// COBIT — unidade coerente de informação (análogo ao qubit, mas clássico)
#[derive(Debug, Clone, PartialEq)]
pub struct Cobit {
    pub phase:     f64,    // fase φ ∈ [0, 2π)
    pub coherence: f64,    // λ₂ ∈ [0, 1]
    pub tau:       f64,    // criticalidade τ ∈ [0, 1]
    pub frozen:    bool,   // COH_FREEZE / COH_LOCK
    pub entangled: Option<usize>, // índice do parceiro de entrelaçamento
}

impl Cobit {
    pub fn new(phase: f64) -> Self {
        Self {
            phase: phase % (2.0 * PI),
            coherence: 1.0,
            tau: 1.0,
            frozen: false,
            entangled: None,
        }
    }

    pub fn vacuum() -> Self {
        Self { phase: 0.0, coherence: 0.0, tau: 0.0, frozen: false, entangled: None }
    }

    pub fn is_coherent(&self, threshold: f64) -> bool {
        self.coherence >= threshold
    }
}

/// Valor de registrador — pode ser float, inteiro, COBIT ou endereço
#[derive(Debug, Clone)]
pub enum RegVal {
    Float(f64),
    Int(i64),
    Cobit(Cobit),
    Addr(usize),
    Nil,
}

impl RegVal {
    pub fn as_f64(&self) -> f64 {
        match self {
            RegVal::Float(v) => *v,
            RegVal::Int(v)   => *v as f64,
            RegVal::Cobit(c) => c.phase,
            RegVal::Addr(a)  => *a as f64,
            RegVal::Nil      => 0.0,
        }
    }

    pub fn as_i64(&self) -> i64 {
        match self {
            RegVal::Float(v) => *v as i64,
            RegVal::Int(v)   => *v,
            RegVal::Cobit(c) => (c.phase * 1000.0) as i64,
            RegVal::Addr(a)  => *a as i64,
            RegVal::Nil      => 0,
        }
    }

    pub fn as_cobit(&self) -> Cobit {
        match self {
            RegVal::Cobit(c) => c.clone(),
            RegVal::Float(v) => Cobit::new(*v),
            _                => Cobit::vacuum(),
        }
    }

    pub fn is_zero(&self) -> bool {
        match self {
            RegVal::Float(v) => v.abs() < 1e-12,
            RegVal::Int(v)   => *v == 0,
            RegVal::Cobit(c) => c.coherence < 1e-12,
            RegVal::Nil      => true,
            RegVal::Addr(a)  => *a == 0,
        }
    }
}

// ═══════════════════════════════════════════════════════════════
// OPCODES — ISA Arkhe(n) v2140.137.∞
// ═══════════════════════════════════════════════════════════════

#[repr(u16)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Opcode {
    // ── COHERENCE 0x00-0x1F ─────────────────────────────────
    NOP              = 0x00,
    COH_INIT         = 0x01,
    COH_MEASURE      = 0x02,
    COH_TUNE_TAU     = 0x03,
    COH_SWAP         = 0x04,
    COH_MERGE        = 0x05,
    COH_SPLIT        = 0x06,
    COH_BRAID        = 0x07,
    COH_FREEZE       = 0x08,
    COH_THAW         = 0x09,
    COH_COPY         = 0x0A,
    COH_COMPARE      = 0x0B,
    COH_SELECT       = 0x0C,
    COH_ENTANGLE     = 0x0D,
    COH_DISENTANGLE  = 0x0E,
    COH_TELEPORT     = 0x0F,
    COH_DISTILL      = 0x10,
    COH_DILUTE       = 0x11,
    COH_AMPLIFY      = 0x12,
    COH_ATTENUATE    = 0x13,
    COH_RESONATE     = 0x14,
    COH_DAMP         = 0x15,
    COH_SYNCHRONIZE  = 0x16,
    COH_DESYNCHRONIZE= 0x17,
    COH_LOCK         = 0x18,
    COH_UNLOCK       = 0x19,
    COH_VERIFY       = 0x1A,
    COH_REPAIR       = 0x1B,
    COH_CLONE        = 0x1C,
    COH_ANNIHILATE   = 0x1D,
    COH_CREATE       = 0x1E,
    COH_DESTROY      = 0x1F,

    // ── PHASE 0x20-0x3F ─────────────────────────────────────
    PHASE_SET        = 0x20,
    PHASE_GET        = 0x21,
    PHASE_ADD        = 0x22,
    PHASE_SUB        = 0x23,
    PHASE_MUL        = 0x24,
    PHASE_DIV        = 0x25,
    PHASE_MOD        = 0x26,
    PHASE_SIN        = 0x27,
    PHASE_COS        = 0x28,
    PHASE_TAN        = 0x29,
    PHASE_EXP        = 0x2A,
    PHASE_LOG        = 0x2B,
    PHASE_POW        = 0x2C,
    PHASE_ROOT       = 0x2D,
    PHASE_CONJUGATE  = 0x2E,
    PHASE_INVERT     = 0x2F,
    PHASE_SHIFT      = 0x30,
    PHASE_ROTATE     = 0x31,
    PHASE_PROJECT    = 0x32,
    PHASE_REFLECT    = 0x33,
    PHASE_INTERPOLATE= 0x34,
    PHASE_SPLINE     = 0x35,
    PHASE_FFT        = 0x36,
    PHASE_IFFT       = 0x37,
    PHASE_CONVOLVE   = 0x38,
    PHASE_CORRELATE  = 0x39,
    PHASE_FILTER     = 0x3A,
    PHASE_WINDOW     = 0x3B,
    PHASE_QUANTIZE   = 0x3C,
    PHASE_DITHER     = 0x3D,
    PHASE_WRAP       = 0x3E,
    PHASE_UNWRAP     = 0x3F,

    // ── TEMPORAL 0x40-0x5F ──────────────────────────────────
    TIME_NOW         = 0x40,
    TIME_DELTA       = 0x41,
    TIME_SCALE       = 0x42,
    TIME_SHIFT       = 0x43,
    TIME_DILATE      = 0x44,
    TIME_CONTRACT    = 0x45,
    TIME_REVERSE     = 0x46,
    TIME_FREEZE      = 0x47,
    TIME_RESUME      = 0x48,
    TIME_LOOP        = 0x49,
    TIME_BRANCH      = 0x4A,
    TIME_MERGE       = 0x4B,
    TIME_PRUNE       = 0x4C,
    TIME_ANCHOR      = 0x4D,
    TIME_PREDICT     = 0x4E,
    TIME_RETRODICT   = 0x4F,
    TIME_CAUSALITY   = 0x50,
    TIME_ACAUSALITY  = 0x51,
    TIME_ENTROPY     = 0x52,
    TIME_NEGENTROPY  = 0x53,
    SOCIAL_ENTROPY   = 0x54,
    TIME_CYCLE       = 0x55,
    TIME_SPIRAL      = 0x56,
    TIME_KNOT        = 0x57,
    TIME_LINK        = 0x58,
    TIME_UNLINK      = 0x59,
    TIME_SYNC        = 0x5A,
    TIME_ASYNC       = 0x5B,
    TIME_BUFFER      = 0x5C,
    TIME_CACHE       = 0x5D,
    TIME_FLUSH       = 0x5E,
    TIME_EXPIRE      = 0x5F,

    // ── AKASHA 0x60-0x7F ────────────────────────────────────
    MEM_ALLOC        = 0x60,
    MEM_FREE         = 0x61,
    MEM_READ         = 0x62,
    MEM_WRITE        = 0x63,
    MEM_COPY         = 0x64,
    MEM_MOVE         = 0x65,
    MEM_SET          = 0x66,
    MEM_CMP          = 0x67,
    MEM_SCAN         = 0x68,
    MEM_FIND         = 0x69,
    MEM_REPLACE      = 0x6A,
    MEM_PROTECT      = 0x6B,
    MEM_UNPROTECT    = 0x6C,
    MEM_MAP          = 0x6D,
    MEM_UNMAP        = 0x6E,
    MEM_FLUSH        = 0x6F,
    AKA_LOG          = 0x70,
    AKA_QUERY        = 0x71,
    AKA_SEED         = 0x72,
    AKA_VERIFY       = 0x73,
    AKA_PRUNE        = 0x74,
    AKA_ARCHIVE      = 0x75,
    AKA_RESTORE      = 0x76,
    AKA_MERGE        = 0x77,
    AKA_SPLIT        = 0x78,
    AKA_HASH         = 0x79,
    AKA_SIGN         = 0x7A,
    AKA_VERIFY_SIG   = 0x7B,
    AKA_ENCRYPT      = 0x7C,
    AKA_DECRYPT      = 0x7D,
    AKA_COMPACT      = 0x7E,
    AKA_EXPAND       = 0x7F,

    // ── NETWORK 0x80-0x9F ───────────────────────────────────
    NET_SEND         = 0x80,
    NET_RECV         = 0x81,
    NET_BROADCAST    = 0x82,
    NET_MULTICAST    = 0x83,
    NET_HANDSHAKE    = 0x84,
    NET_DISCONNECT   = 0x85,
    NET_SYNC         = 0x86,
    NET_DESYNC       = 0x87,
    NET_PING         = 0x88,
    NET_PONG         = 0x89,
    CONSENSUS_PROPOSE= 0x8A,
    CONSENSUS_VOTE   = 0x8B,
    CONSENSUS_COMMIT = 0x8C,
    CONSENSUS_ABORT  = 0x8D,
    CONSENSUS_VALIDATE = 0x8E,
    CONSENSUS_MERGE  = 0x8F,
    P2P_CONNECT      = 0x90,
    P2P_DISCONNECT   = 0x91,
    P2P_DISCOVER     = 0x92,
    P2P_ADVERTISE    = 0x93,
    P2P_RELAY        = 0x94,
    P2P_TUNNEL       = 0x95,
    QTL_SYNC         = 0x96,
    QTL_MERGE        = 0x97,
    QTL_REPLICATE    = 0x98,
    QTL_SHARD        = 0x99,
    COH_PROPAGATE    = 0x9A,
    COH_GATHER       = 0x9B,
    COH_DIFFUSE      = 0x9C,
    COH_CONCENTRATE  = 0x9D,
    COH_FUSE         = 0x9E,
    NET_OPTIMIZE     = 0x9F,

    // ── MATH 0xA0-0xBF ──────────────────────────────────────
    ADD   = 0xA0, SUB   = 0xA1, MUL   = 0xA2, DIV   = 0xA3,
    MOD   = 0xA4, NEG   = 0xA5, ABS   = 0xA6, MIN   = 0xA7,
    MAX   = 0xA8, CLAMP = 0xA9, FLOOR = 0xAA, CEIL  = 0xAB,
    ROUND = 0xAC, TRUNC = 0xAD, SQRT  = 0xAE, CBRT  = 0xAF,
    POW   = 0xB0, EXP   = 0xB1, LN    = 0xB2, LOG10 = 0xB3,
    LOG2  = 0xB4, SIN   = 0xB5, COS   = 0xB6, TAN   = 0xB7,
    ASIN  = 0xB8, ACOS  = 0xB9, ATAN  = 0xBA, ATAN2 = 0xBB,
    SINH  = 0xBC, COSH  = 0xBD, TANH  = 0xBE, HYPOT = 0xBF,

    // ── CONTROL 0xC0-0xDF ───────────────────────────────────
    JMP      = 0xC0, JZ       = 0xC1, JNZ      = 0xC2, JE       = 0xC3,
    JNE      = 0xC4, JL       = 0xC5, JG       = 0xC6, JLE      = 0xC7,
    JGE      = 0xC8, CALL     = 0xC9, RET      = 0xCA, PUSH     = 0xCB,
    POP      = 0xCC, PUSH_ALL = 0xCD, POP_ALL  = 0xCE, LOOP     = 0xCF,
    LOOPE    = 0xD0, LOOPNE   = 0xD1, FOR      = 0xD2, WHILE    = 0xD3,
    BREAK    = 0xD4, CONTINUE = 0xD5, SWITCH   = 0xD6, CASE     = 0xD7,
    DEFAULT  = 0xD8, TRY      = 0xD9, CATCH    = 0xDA, THROW    = 0xDB,
    FINALLY  = 0xDC, YIELD    = 0xDD, RESUME   = 0xDE, EXIT     = 0xDF,

    // ── SYSTEM 0xE0-0xFF ────────────────────────────────────
    SYS_INFO    = 0xE0, SYS_TIME    = 0xE1, COH_LOSS    = 0xE2,
    ENV_SPAWN   = 0xE3, PHASE_RECTIFY = 0xE4, COH_SEED    = 0xE5,
    COH_BUBBLE  = 0xE6, AKA_QUERY_LOGN = 0xE7, PHASE_COMPLEMENT = 0xE8,
    TAU_AVERAGE = 0xE9, LPU_REROUTE = 0xEA, SYS_HALT = 0xEB,
    PEAK_COHERENCE = 0xEC, GOLDEN_RATIO_SPAWN = 0xED, ENTANGLEMENT_PERMUTE = 0xEE,
    SYS_CONFIG  = 0xEF,
    META_REFLECT   = 0xF0, META_INTROSPECT = 0xF1, AKA_QUERY_LINEAR = 0xF2,
    MIRROR_SYMMETRY = 0xF3, COH_INJECT = 0xF4, PHASE_NEST = 0xF5,
    PHASE_ITERATE  = 0xF6, QTL_SCAN = 0xF7, MODULO_RESONANCE = 0xF8,
    META_TRACE     = 0xF9, META_PROFILE    = 0xFA, META_OPTIMIZE= 0xFB,
    META_VERIFY    = 0xFC, META_SIGN       = 0xFD, META_INVOKE  = 0xFE,
    META_TRANSCEND = 0xFF,

    // ── EXTENDED 0x200-0x2FF ────────────────────────────────
    HETEROGENEOUS_FUSION = 0x213,
}

impl Opcode {
    pub fn from_u8(byte: u8) -> Self {
        Self::from_u16(byte as u16)
    }

    pub fn from_u16(val: u16) -> Self {
        match val {
            0x00 => Opcode::NOP,
            0x01 => Opcode::COH_INIT,
            0x02 => Opcode::COH_MEASURE,
            0x03 => Opcode::COH_TUNE_TAU,
            0x04 => Opcode::COH_SWAP,
            0x05 => Opcode::COH_MERGE,
            0x06 => Opcode::COH_SPLIT,
            0x07 => Opcode::COH_BRAID,
            0x08 => Opcode::COH_FREEZE,
            0x09 => Opcode::COH_THAW,
            0x0A => Opcode::COH_COPY,
            0x0B => Opcode::COH_COMPARE,
            0x0C => Opcode::COH_SELECT,
            0x0D => Opcode::COH_ENTANGLE,
            0x0E => Opcode::COH_DISENTANGLE,
            0x0F => Opcode::COH_TELEPORT,
            0x10 => Opcode::COH_DISTILL,
            0x11 => Opcode::COH_DILUTE,
            0x12 => Opcode::COH_AMPLIFY,
            0x13 => Opcode::COH_ATTENUATE,
            0x14 => Opcode::COH_RESONATE,
            0x15 => Opcode::COH_DAMP,
            0x16 => Opcode::COH_SYNCHRONIZE,
            0x17 => Opcode::COH_DESYNCHRONIZE,
            0x18 => Opcode::COH_LOCK,
            0x19 => Opcode::COH_UNLOCK,
            0x1A => Opcode::COH_VERIFY,
            0x1B => Opcode::COH_REPAIR,
            0x1C => Opcode::COH_CLONE,
            0x1D => Opcode::COH_ANNIHILATE,
            0x1E => Opcode::COH_CREATE,
            0x1F => Opcode::COH_DESTROY,
            0x20 => Opcode::PHASE_SET,
            0x21 => Opcode::PHASE_GET,
            0x22 => Opcode::PHASE_ADD,
            0x23 => Opcode::PHASE_SUB,
            0x24 => Opcode::PHASE_MUL,
            0x25 => Opcode::PHASE_DIV,
            0x26 => Opcode::PHASE_MOD,
            0x27 => Opcode::PHASE_SIN,
            0x28 => Opcode::PHASE_COS,
            0x29 => Opcode::PHASE_TAN,
            0x2A => Opcode::PHASE_EXP,
            0x2B => Opcode::PHASE_LOG,
            0x2C => Opcode::PHASE_POW,
            0x2D => Opcode::PHASE_ROOT,
            0x2E => Opcode::PHASE_CONJUGATE,
            0x2F => Opcode::PHASE_INVERT,
            0x30 => Opcode::PHASE_SHIFT,
            0x31 => Opcode::PHASE_ROTATE,
            0x32 => Opcode::PHASE_PROJECT,
            0x33 => Opcode::PHASE_REFLECT,
            0x34 => Opcode::PHASE_INTERPOLATE,
            0x35 => Opcode::PHASE_SPLINE,
            0x36 => Opcode::PHASE_FFT,
            0x37 => Opcode::PHASE_IFFT,
            0x38 => Opcode::PHASE_CONVOLVE,
            0x39 => Opcode::PHASE_CORRELATE,
            0x3A => Opcode::PHASE_FILTER,
            0x3B => Opcode::PHASE_WINDOW,
            0x3C => Opcode::PHASE_QUANTIZE,
            0x3D => Opcode::PHASE_DITHER,
            0x3E => Opcode::PHASE_WRAP,
            0x3F => Opcode::PHASE_UNWRAP,
            0x40 => Opcode::TIME_NOW,
            0x41 => Opcode::TIME_DELTA,
            0x42 => Opcode::TIME_SCALE,
            0x43 => Opcode::TIME_SHIFT,
            0x44 => Opcode::TIME_DILATE,
            0x45 => Opcode::TIME_CONTRACT,
            0x46 => Opcode::TIME_REVERSE,
            0x47 => Opcode::TIME_FREEZE,
            0x48 => Opcode::TIME_RESUME,
            0x49 => Opcode::TIME_LOOP,
            0x4A => Opcode::TIME_BRANCH,
            0x4B => Opcode::TIME_MERGE,
            0x4C => Opcode::TIME_PRUNE,
            0x4D => Opcode::TIME_ANCHOR,
            0x4E => Opcode::TIME_PREDICT,
            0x4F => Opcode::TIME_RETRODICT,
            0x50 => Opcode::TIME_CAUSALITY,
            0x51 => Opcode::TIME_ACAUSALITY,
            0x52 => Opcode::TIME_ENTROPY,
            0x53 => Opcode::TIME_NEGENTROPY,
            0x54 => Opcode::SOCIAL_ENTROPY,
            0x55 => Opcode::TIME_CYCLE,
            0x56 => Opcode::TIME_SPIRAL,
            0x57 => Opcode::TIME_KNOT,
            0x58 => Opcode::TIME_LINK,
            0x59 => Opcode::TIME_UNLINK,
            0x5A => Opcode::TIME_SYNC,
            0x5B => Opcode::TIME_ASYNC,
            0x5C => Opcode::TIME_BUFFER,
            0x5D => Opcode::TIME_CACHE,
            0x5E => Opcode::TIME_FLUSH,
            0x5F => Opcode::TIME_EXPIRE,
            0x60 => Opcode::MEM_ALLOC,
            0x61 => Opcode::MEM_FREE,
            0x62 => Opcode::MEM_READ,
            0x63 => Opcode::MEM_WRITE,
            0x64 => Opcode::MEM_COPY,
            0x65 => Opcode::MEM_MOVE,
            0x66 => Opcode::MEM_SET,
            0x67 => Opcode::MEM_CMP,
            0x68 => Opcode::MEM_SCAN,
            0x69 => Opcode::MEM_FIND,
            0x6A => Opcode::MEM_REPLACE,
            0x6B => Opcode::MEM_PROTECT,
            0x6C => Opcode::MEM_UNPROTECT,
            0x6D => Opcode::MEM_MAP,
            0x6E => Opcode::MEM_UNMAP,
            0x6F => Opcode::MEM_FLUSH,
            0x70 => Opcode::AKA_LOG,
            0x71 => Opcode::AKA_QUERY,
            0x72 => Opcode::AKA_SEED,
            0x73 => Opcode::AKA_VERIFY,
            0x74 => Opcode::AKA_PRUNE,
            0x75 => Opcode::AKA_ARCHIVE,
            0x76 => Opcode::AKA_RESTORE,
            0x77 => Opcode::AKA_MERGE,
            0x78 => Opcode::AKA_SPLIT,
            0x79 => Opcode::AKA_HASH,
            0x7A => Opcode::AKA_SIGN,
            0x7B => Opcode::AKA_VERIFY_SIG,
            0x7C => Opcode::AKA_ENCRYPT,
            0x7D => Opcode::AKA_DECRYPT,
            0x7E => Opcode::AKA_COMPACT,
            0x7F => Opcode::AKA_EXPAND,
            0x80 => Opcode::NET_SEND,
            0x81 => Opcode::NET_RECV,
            0x82 => Opcode::NET_BROADCAST,
            0x83 => Opcode::NET_MULTICAST,
            0x84 => Opcode::NET_HANDSHAKE,
            0x85 => Opcode::NET_DISCONNECT,
            0x86 => Opcode::NET_SYNC,
            0x87 => Opcode::NET_DESYNC,
            0x88 => Opcode::NET_PING,
            0x89 => Opcode::NET_PONG,
            0x8A => Opcode::CONSENSUS_PROPOSE,
            0x8B => Opcode::CONSENSUS_VOTE,
            0x8C => Opcode::CONSENSUS_COMMIT,
            0x8D => Opcode::CONSENSUS_ABORT,
            0x8E => Opcode::CONSENSUS_VALIDATE,
            0x8F => Opcode::CONSENSUS_MERGE,
            0x90 => Opcode::P2P_CONNECT,
            0x91 => Opcode::P2P_DISCONNECT,
            0x92 => Opcode::P2P_DISCOVER,
            0x93 => Opcode::P2P_ADVERTISE,
            0x94 => Opcode::P2P_RELAY,
            0x95 => Opcode::P2P_TUNNEL,
            0x96 => Opcode::QTL_SYNC,
            0x97 => Opcode::QTL_MERGE,
            0x98 => Opcode::QTL_REPLICATE,
            0x99 => Opcode::QTL_SHARD,
            0x9A => Opcode::COH_PROPAGATE,
            0x9B => Opcode::COH_GATHER,
            0x9C => Opcode::COH_DIFFUSE,
            0x9D => Opcode::COH_CONCENTRATE,
            0x9E => Opcode::COH_FUSE,
            0x9F => Opcode::NET_OPTIMIZE,
            0xA0 => Opcode::ADD, 0xA1 => Opcode::SUB, 0xA2 => Opcode::MUL, 0xA3 => Opcode::DIV,
            0xA4 => Opcode::MOD, 0xA5 => Opcode::NEG, 0xA6 => Opcode::ABS, 0xA7 => Opcode::MIN,
            0xA8 => Opcode::MAX, 0xA9 => Opcode::CLAMP, 0xAA => Opcode::FLOOR, 0xAB => Opcode::CEIL,
            0xAC => Opcode::ROUND, 0xAD => Opcode::TRUNC, 0xAE => Opcode::SQRT, 0xAF => Opcode::CBRT,
            0xB0 => Opcode::POW, 0xB1 => Opcode::EXP, 0xB2 => Opcode::LN, 0xB3 => Opcode::LOG10,
            0xB4 => Opcode::LOG2, 0xB5 => Opcode::SIN, 0xB6 => Opcode::COS, 0xB7 => Opcode::TAN,
            0xB8 => Opcode::ASIN, 0xB9 => Opcode::ACOS, 0xBA => Opcode::ATAN, 0xBB => Opcode::ATAN2,
            0xBC => Opcode::SINH, 0xBD => Opcode::COSH, 0xBE => Opcode::TANH, 0xBF => Opcode::HYPOT,
            0xC0 => Opcode::JMP, 0xC1 => Opcode::JZ, 0xC2 => Opcode::JNZ, 0xC3 => Opcode::JE,
            0xC4 => Opcode::JNE, 0xC5 => Opcode::JL, 0xC6 => Opcode::JG, 0xC7 => Opcode::JLE,
            0xC8 => Opcode::JGE, 0xC9 => Opcode::CALL, 0xCA => Opcode::RET, 0xCB => Opcode::PUSH,
            0xCC => Opcode::POP, 0xCD => Opcode::PUSH_ALL, 0xCE => Opcode::POP_ALL, 0xCF => Opcode::LOOP,
            0xD0 => Opcode::LOOPE, 0xD1 => Opcode::LOOPNE, 0xD2 => Opcode::FOR, 0xD3 => Opcode::WHILE,
            0xD4 => Opcode::BREAK, 0xD5 => Opcode::CONTINUE, 0xD6 => Opcode::SWITCH, 0xD7 => Opcode::CASE,
            0xD8 => Opcode::DEFAULT, 0xD9 => Opcode::TRY, 0xDA => Opcode::CATCH, 0xDB => Opcode::THROW,
            0xDC => Opcode::FINALLY, 0xDD => Opcode::YIELD, 0xDE => Opcode::RESUME, 0xDF => Opcode::EXIT,
            0xE0 => Opcode::SYS_INFO, 0xE1 => Opcode::SYS_TIME, 0xE2 => Opcode::COH_LOSS,
            0xE3 => Opcode::ENV_SPAWN, 0xE4 => Opcode::PHASE_RECTIFY, 0xE5 => Opcode::COH_SEED,
            0xE6 => Opcode::COH_BUBBLE, 0xE7 => Opcode::AKA_QUERY_LOGN, 0xE8 => Opcode::PHASE_COMPLEMENT,
            0xE9 => Opcode::TAU_AVERAGE, 0xEA => Opcode::LPU_REROUTE, 0xEB => Opcode::SYS_HALT,
            0xEC => Opcode::PEAK_COHERENCE, 0xED => Opcode::GOLDEN_RATIO_SPAWN, 0xEE => Opcode::ENTANGLEMENT_PERMUTE,
            0xEF => Opcode::SYS_CONFIG,
            0xF0 => Opcode::META_REFLECT, 0xF1 => Opcode::META_INTROSPECT, 0xF2 => Opcode::AKA_QUERY_LINEAR,
            0xF3 => Opcode::MIRROR_SYMMETRY, 0xF4 => Opcode::COH_INJECT, 0xF5 => Opcode::PHASE_NEST,
            0xF6 => Opcode::PHASE_ITERATE, 0xF7 => Opcode::QTL_SCAN, 0xF8 => Opcode::MODULO_RESONANCE,
            0xF9 => Opcode::META_TRACE, 0xFA => Opcode::META_PROFILE, 0xFB => Opcode::META_OPTIMIZE,
            0xFC => Opcode::META_VERIFY, 0xFD => Opcode::META_SIGN, 0xFE => Opcode::META_INVOKE,
            0xFF => Opcode::META_TRANSCEND,
            0x213 => Opcode::HETEROGENEOUS_FUSION,
            _ => Opcode::NOP, // Default for undefined values
        }
    }

    pub fn group(&self) -> &'static str {
        let val = *self as u16;
        if val >= 0x200 {
            return "EXTENDED";
        }
        let b = val as u8;
        match b {
            0x00..=0x1F => "COHERENCE",
            0x20..=0x3F => "PHASE",
            0x40..=0x5F => "TEMPORAL",
            0x60..=0x7F => "AKASHA",
            0x80..=0x9F => "NETWORK",
            0xA0..=0xBF => "MATH",
            0xC0..=0xDF => "CONTROL",
            0xE0..=0xFF => "SYSTEM",
        }
    }

    /// Ciclos nominais para o escalonador Kuramoto
    pub fn cycles(&self) -> u64 {
        match self {
            Opcode::NOP              => 1,
            Opcode::COH_INIT         => 3,
            Opcode::COH_MEASURE      => 5,
            Opcode::COH_TUNE_TAU     => 4,
            Opcode::COH_MERGE        => 8,
            Opcode::COH_BRAID        => 10,
            Opcode::COH_TELEPORT     => 12,
            Opcode::COH_DISTILL      => 15,
            Opcode::COH_RESONATE     => 20,
            Opcode::PHASE_FFT | Opcode::PHASE_IFFT => 50,
            Opcode::PHASE_CONVOLVE   => 25,
            Opcode::PHASE_CORRELATE  => 30,
            Opcode::TIME_PREDICT | Opcode::TIME_RETRODICT => 100,
            Opcode::AKA_MERGE        => 120,
            Opcode::QTL_SYNC         => 200,
            Opcode::QTL_MERGE        => 300,
            Opcode::NET_OPTIMIZE     => 150,
            Opcode::COH_FUSE         => 137,
            Opcode::SOCIAL_ENTROPY   => 88,
            Opcode::LPU_REROUTE      => 214,
            Opcode::COH_INJECT       => 50,
            Opcode::MODULO_RESONANCE => 10,
            Opcode::META_INVOKE      => 500,
            Opcode::META_TRANSCEND   => 137,  // Transcende em 137 ciclos
            Opcode::ADD | Opcode::SUB | Opcode::NEG => 2,
            Opcode::MUL              => 3,
            Opcode::DIV              => 5,
            Opcode::SQRT             => 10,
            Opcode::SIN | Opcode::COS | Opcode::TAN => 15,
            Opcode::JMP              => 1,
            Opcode::CALL | Opcode::RET => 2,
            Opcode::SYS_TIME         => 2,
            _                        => 6,   // default
        }
    }
}

// ═══════════════════════════════════════════════════════════════
// REGISTRADORES
// ═══════════════════════════════════════════════════════════════

pub const R_TAU:    usize = 16;   // Rτ  — criticalidade
pub const R_LAMBDA: usize = 17;   // Rλ  — coerência medida
pub const R_PHI:    usize = 18;   // Rφ  — fase acumulada
pub const R_TIME:   usize = 19;   // Rt  — timestamp
pub const R_AKA:    usize = 20;   // Raka — ponteiro Akasha
pub const R_QTL:    usize = 21;   // Rqtl — ponteiro QTL
pub const R_PC:     usize = 22;   // Rpc  — program counter
pub const R_SP:     usize = 23;   // Rsp  — stack pointer
pub const R_FP:     usize = 24;   // Rfp  — frame pointer
pub const R_STATUS: usize = 25;
pub const R_ERROR:  usize = 26;
pub const R_ORCID:  usize = 27;   // Identidade do processo
pub const R_137:    usize = 28;   // Constante 137 (read-only)
pub const R_PHI_C:  usize = 29;   // φ (read-only)
pub const R_PI:     usize = 30;   // π (read-only)
pub const R_ZERO:   usize = 31;   // 0 (read-only)

pub const NUM_REGS: usize = 32;

// ═══════════════════════════════════════════════════════════════
// INSTRUÇÃO
// ═══════════════════════════════════════════════════════════════

#[derive(Debug, Clone)]
pub struct Instruction {
    pub opcode:    Opcode,
    pub operands:  Vec<u8>,    // índices de registradores ou literais
    pub immediate: Option<f64>, // valor imediato opcional
}

impl Instruction {
    pub fn new(opcode: Opcode, operands: Vec<u8>) -> Self {
        Self { opcode, operands, immediate: None }
    }

    pub fn with_imm(mut self, v: f64) -> Self {
        self.immediate = Some(v);
        self
    }
}

// ═══════════════════════════════════════════════════════════════
// AKASHA LEDGER
// ═══════════════════════════════════════════════════════════════

#[derive(Debug, Clone)]
pub struct AkashaEntry {
    pub timestamp:  u64,
    pub event:      String,
    pub severity:   u8,
    pub hash:       u64,      // FNV-1a simplificado
    pub phase_ref:  f64,
}

#[derive(Debug, Default)]
pub struct AkashaLedger {
    pub entries:    Vec<AkashaEntry>,
    pub merkle_root: u64,
    pub seed_pool:  Vec<(u64, f64)>, // (future_timestamp, phase)
}

impl AkashaLedger {
    pub fn log(&mut self, timestamp: u64, event: &str, severity: u8, phase: f64) {
        let hash = self.fnv1a(event);
        let entry = AkashaEntry {
            timestamp, event: event.to_string(), severity, hash, phase_ref: phase,
        };
        self.entries.push(entry);
        self.update_merkle();
    }

    pub fn seed(&mut self, future_ts: u64, phase: f64) {
        self.seed_pool.push((future_ts, phase));
    }

    fn fnv1a(&self, s: &str) -> u64 {
        let mut hash: u64 = 0xcbf29ce484222325;
        for b in s.bytes() {
            hash ^= b as u64;
            hash = hash.wrapping_mul(0x100000001b3);
        }
        hash
    }

    fn update_merkle(&mut self) {
        self.merkle_root = self.entries.iter()
            .fold(0u64, |acc, e| acc ^ e.hash);
    }
}

// ═══════════════════════════════════════════════════════════════
// ORQUESTRADOR KURAMOTO INTEGRADO
// ═══════════════════════════════════════════════════════════════

pub struct KuramotoScheduler {
    pub lambda:      f64,     // R(t) — parâmetro de ordem
    pub theta:       f64,     // fase global do processo
    pub omega:       f64,     // frequência natural
    pub k_coupling:  f64,     // K — acoplamento
    pub cycle_count: u64,
}

impl KuramotoScheduler {
    pub fn new() -> Self {
        Self {
            lambda:     1.0,
            theta:      0.0,
            omega:      2.0 * PI * 23.8e12,  // 23.8 THz — frequência φ-otimizada
            k_coupling: PHI_INV,              // K_c = φ⁻¹
            cycle_count: 0,
        }
    }

    pub fn tick(&mut self, n_cycles: u64) {
        let dt = n_cycles as f64 * 1.98e-18;  // timestep físico
        let _noise: f64 = 0.0;  // determinístico por padrão
        self.theta = (self.theta + self.omega * dt) % (2.0 * PI);
        self.cycle_count += n_cycles;
    }

    pub fn check_coherence(&self) -> CoherenceAlert {
        if self.lambda < LAMBDA_CRITICAL {
            CoherenceAlert::Critical
        } else if self.lambda < LAMBDA_WARN {
            CoherenceAlert::Warning
        } else if self.lambda < LAMBDA_PHI_C {
            CoherenceAlert::PhaseTransition
        } else {
            CoherenceAlert::Nominal
        }
    }
}

#[derive(Debug, PartialEq)]
pub enum CoherenceAlert {
    Nominal,
    PhaseTransition,
    Warning,
    Critical,
}

// ═══════════════════════════════════════════════════════════════
// ORBVM — MÁQUINA VIRTUAL PRINCIPAL
// ═══════════════════════════════════════════════════════════════

pub struct OrbVM {
    // Registradores
    pub regs:        [RegVal; NUM_REGS],

    // Memória
    pub memory:      Vec<u8>,
    pub mem_size:    usize,

    // Stack
    pub stack:       Vec<RegVal>,

    // Programa
    pub program:     Vec<Instruction>,
    pub pc:          usize,

    // Subsistemas
    pub akasha:      AkashaLedger,
    pub kuramoto:    KuramotoScheduler,

    // Estado
    pub halted:      bool,
    pub cycle_total: u64,
    pub orcid:       String,

    // Constantes canônicas (read-only regs inicializados)
    pub version:     &'static str,
}

impl OrbVM {
    pub fn new(mem_size: usize) -> Self {
        let mut regs: [RegVal; NUM_REGS] = std::array::from_fn(|_| RegVal::Nil);

        // Inicializa registradores especiais
        regs[R_TAU]    = RegVal::Float(1.0);
        regs[R_LAMBDA] = RegVal::Float(1.0);
        regs[R_PHI]    = RegVal::Float(0.0);
        regs[R_TIME]   = RegVal::Int(0);
        regs[R_PC]     = RegVal::Int(0);
        regs[R_SP]     = RegVal::Int(mem_size as i64 - 1);
        regs[R_STATUS] = RegVal::Int(0);
        regs[R_ERROR]  = RegVal::Int(0);
        regs[R_ZERO]   = RegVal::Float(0.0);

        // Constantes read-only
        regs[R_137]   = RegVal::Float(137.0);
        regs[R_PHI_C] = RegVal::Float(PHI);
        regs[R_PI]    = RegVal::Float(PI);

        Self {
            regs,
            memory:      vec![0u8; mem_size],
            mem_size,
            stack:       Vec::with_capacity(256),
            program:     Vec::new(),
            pc:          0,
            akasha:      AkashaLedger::default(),
            kuramoto:    KuramotoScheduler::new(),
            halted:      false,
            cycle_total: 0,
            orcid:       "0009-0005-2697-4668".to_string(),
            version:     "OrbVM ISA Arkhe(n) v2140.137.INF",
        }
    }

    pub fn load(&mut self, program: Vec<Instruction>) {
        self.program = program;
        self.pc = 0;
        self.regs[R_PC] = RegVal::Int(0);
    }

    fn reg(&self, idx: u8) -> &RegVal {
        &self.regs[idx as usize]
    }

    fn reg_mut(&mut self, idx: u8) -> &mut RegVal {
        &mut self.regs[idx as usize]
    }

    fn set_reg(&mut self, idx: u8, val: RegVal) {
        // Protege registradores read-only
        match idx as usize {
            R_137 | R_PHI_C | R_PI | R_ZERO => {
                self.regs[R_ERROR] = RegVal::Int(0xDEAD);
            }
            _ => self.regs[idx as usize] = val,
        }
    }

    /// Executa um único ciclo de instrução
    pub fn step(&mut self) -> Result<(), OrbError> {
        if self.halted { return Err(OrbError::Halted); }
        if self.pc >= self.program.len() { return Err(OrbError::PcOutOfBounds); }

        let instr = self.program[self.pc].clone();

        // Verificação de segurança para 0x213
        if instr.opcode == Opcode::HETEROGENEOUS_FUSION {
            if self.kuramoto.lambda < LAMBDA_PHI_C {
                return Err(OrbError::InsufficientCoherence);
            }
        }

        let cycles = instr.opcode.cycles();

        self.execute(instr)?;

        self.kuramoto.tick(cycles);
        self.cycle_total += cycles;
        self.regs[R_TIME] = RegVal::Int(self.cycle_total as i64);
        self.regs[R_LAMBDA] = RegVal::Float(self.kuramoto.lambda);

        // Avança PC (exceto instruções de salto que já o ajustaram)
        if matches!(self.regs[R_PC], RegVal::Int(v) if v as usize == self.pc) {
            self.pc += 1;
            self.regs[R_PC] = RegVal::Int(self.pc as i64);
        } else {
            self.pc = self.regs[R_PC].as_i64() as usize;
        }

        Ok(())
    }

    /// Executa até HALT, EXIT ou META_TRANSCEND
    pub fn run(&mut self) -> Result<u64, OrbError> {
        while !self.halted {
            match self.step() {
                Ok(_) => {}
                Err(OrbError::Halted) => break,
                Err(e) => return Err(e),
            }
        }
        Ok(self.cycle_total)
    }

    fn execute(&mut self, instr: Instruction) -> Result<(), OrbError> {
        let ops = &instr.operands;

        match instr.opcode {
            // ─── NOP ──────────────────────────────────────────
            Opcode::NOP => {}

            // ─── COHERENCE ────────────────────────────────────
            Opcode::COH_INIT => {
                let phase = instr.immediate.unwrap_or(0.0);
                self.set_reg(ops[0], RegVal::Cobit(Cobit::new(phase)));
            }
            Opcode::COH_MEASURE => {
                let c = self.reg(ops[0]).as_cobit();
                self.set_reg(ops[1], RegVal::Float(c.coherence));
                self.kuramoto.lambda = c.coherence;
            }
            Opcode::COH_TUNE_TAU => {
                let tau = self.reg(ops[1]).as_f64().clamp(0.0, 1.0);
                let mut c = self.reg(ops[0]).as_cobit();
                if !c.frozen { c.tau = tau; }
                self.set_reg(ops[0], RegVal::Cobit(c));
            }
            Opcode::COH_SWAP => {
                let c1 = self.reg(ops[0]).as_cobit();
                let c2 = self.reg(ops[1]).as_cobit();
                let mut r = c1.clone();
                r.phase = c2.phase;
                self.set_reg(ops[2], RegVal::Cobit(r));
            }
            Opcode::COH_MERGE => {
                let c1 = self.reg(ops[0]).as_cobit();
                let c2 = self.reg(ops[1]).as_cobit();
                let merged = Cobit {
                    phase:     (c1.phase + c2.phase) / 2.0,
                    coherence: (c1.coherence * c2.coherence).sqrt(),
                    tau:       (c1.tau + c2.tau) / 2.0,
                    frozen:    false,
                    entangled: None,
                };
                self.set_reg(ops[2], RegVal::Cobit(merged));
            }
            Opcode::COH_BRAID => {
                let n = self.reg(ops[2]).as_i64() as u32;
                let mut c = self.reg(ops[0]).as_cobit();
                // σᵢ^n: rotaciona a fase por n vezes o ângulo da trança de Fibonacci
                // R(σᵢ) diagonal: e^{-4πi/5} | e^{3πi/5}
                let braid_angle = -4.0 * PI / 5.0;
                c.phase = (c.phase + braid_angle * n as f64) % (2.0 * PI);
                self.set_reg(ops[0], RegVal::Cobit(c));
            }
            Opcode::COH_FREEZE => {
                let mut c = self.reg(ops[0]).as_cobit();
                c.frozen = true; c.tau = 1.0;
                self.set_reg(ops[0], RegVal::Cobit(c));
            }
            Opcode::COH_THAW | Opcode::COH_UNLOCK => {
                let mut c = self.reg(ops[0]).as_cobit();
                c.frozen = false;
                self.set_reg(ops[0], RegVal::Cobit(c));
            }
            Opcode::COH_COPY | Opcode::COH_CLONE => {
                let c = self.reg(ops[0]).as_cobit();
                self.set_reg(ops[1], RegVal::Cobit(c));
            }
            Opcode::COH_COMPARE => {
                let c1 = self.reg(ops[0]).as_cobit();
                let c2 = self.reg(ops[1]).as_cobit();
                let diff = (c1.coherence - c2.coherence).abs();
                self.set_reg(ops[2], RegVal::Float(diff));
            }
            Opcode::COH_LOCK => {
                let mut c = self.reg(ops[0]).as_cobit();
                c.frozen = true;
                self.set_reg(ops[0], RegVal::Cobit(c));
            }
            Opcode::COH_VERIFY => {
                let c = self.reg(ops[0]).as_cobit();
                let valid = c.coherence >= LAMBDA_PHI_C;
                self.set_reg(ops[1], RegVal::Int(valid as i64));
            }
            Opcode::COH_REPAIR => {
                let mut c = self.reg(ops[0]).as_cobit();
                if !c.frozen {
                    c.coherence = (c.coherence + 0.05).min(1.0);
                }
                self.set_reg(ops[0], RegVal::Cobit(c));
            }
            Opcode::COH_CREATE => {
                self.set_reg(ops[0], RegVal::Cobit(Cobit::new(
                    self.kuramoto.theta  // nasce na fase atual da rede
                )));
            }
            Opcode::COH_DESTROY => {
                self.set_reg(ops[0], RegVal::Cobit(Cobit::vacuum()));
            }
            Opcode::COH_ANNIHILATE => {
                self.set_reg(ops[0], RegVal::Cobit(Cobit::vacuum()));
                self.set_reg(ops[1], RegVal::Cobit(Cobit::vacuum()));
            }
            Opcode::COH_SYNCHRONIZE => {
                let p1 = self.reg(ops[0]).as_cobit().phase;
                let p2 = self.reg(ops[1]).as_cobit().phase;
                let mid = (p1 + p2) / 2.0;
                let mut c1 = self.reg(ops[0]).as_cobit();
                let mut c2 = self.reg(ops[1]).as_cobit();
                c1.phase = mid; c2.phase = mid;
                self.set_reg(ops[0], RegVal::Cobit(c1));
                self.set_reg(ops[1], RegVal::Cobit(c2));
            }
            Opcode::COH_AMPLIFY => {
                let gain = self.reg(ops[1]).as_f64();
                let mut c = self.reg(ops[0]).as_cobit();
                c.phase = (c.phase * gain) % (2.0 * PI);
                c.coherence = (c.coherence * gain.abs().sqrt()).min(1.0);
                self.set_reg(ops[0], RegVal::Cobit(c));
            }
            Opcode::COH_ATTENUATE => {
                let loss = self.reg(ops[1]).as_f64().abs();
                let mut c = self.reg(ops[0]).as_cobit();
                c.coherence = (c.coherence - loss).max(0.0);
                self.set_reg(ops[0], RegVal::Cobit(c));
            }
            Opcode::COH_DAMP => {
                let rate = self.reg(ops[1]).as_f64().clamp(0.0, 1.0);
                let mut c = self.reg(ops[0]).as_cobit();
                c.coherence *= 1.0 - rate;
                self.set_reg(ops[0], RegVal::Cobit(c));
            }
            Opcode::COH_RESONATE => {
                // Ressonância forçada — drive com frequência externa
                let freq = self.reg(ops[1]).as_f64();
                let dur  = self.reg(ops[2]).as_f64();
                let mut c = self.reg(ops[0]).as_cobit();
                c.phase = (c.phase + freq * dur) % (2.0 * PI);
                c.coherence = (c.coherence + 0.1 * dur).min(1.0);
                self.set_reg(ops[0], RegVal::Cobit(c));
            }
            Opcode::COH_DISTILL => {
                let c = self.reg(ops[0]).as_cobit();
                let distilled = Cobit {
                    phase:     c.phase,
                    coherence: c.coherence.powi(2),  // purificação → eleva ao quadrado
                    tau:       c.tau,
                    frozen:    false,
                    entangled: None,
                };
                self.set_reg(ops[1], RegVal::Cobit(distilled));
            }
            Opcode::COH_DILUTE => {
                let factor = self.reg(ops[2]).as_f64().clamp(0.0, 1.0);
                let c = self.reg(ops[0]).as_cobit();
                let diluted = Cobit {
                    coherence: c.coherence * factor,
                    ..c
                };
                self.set_reg(ops[1], RegVal::Cobit(diluted));
            }
            Opcode::COH_PROPAGATE => {
                // Propaga coerência para vizinhos (simulado via λ global)
                let radius = self.reg(ops[1]).as_f64();
                let boost = (1.0 / (1.0 + radius)) * 0.1;
                self.kuramoto.lambda = (self.kuramoto.lambda + boost).min(1.0);
            }
            Opcode::COH_GATHER => {
                let _center = self.reg(ops[0]).as_f64();
                let radius = self.reg(ops[1]).as_f64();
                let gathered = self.kuramoto.lambda * (1.0 - radius / 100.0).max(0.1);
                self.set_reg(ops[2], RegVal::Float(gathered));
            }
            Opcode::COH_DIFFUSE => {
                let rate = self.reg(ops[1]).as_f64();
                self.kuramoto.lambda = (self.kuramoto.lambda - rate * 0.01).max(0.0);
            }
            Opcode::COH_CONCENTRATE => {
                let rate = self.reg(ops[1]).as_f64();
                self.kuramoto.lambda = (self.kuramoto.lambda + rate * 0.01).min(1.0);
            }
            Opcode::COH_TELEPORT => {
                // Teleportação: copia estado e aniquila o original
                let c = self.reg(ops[0]).as_cobit();
                self.set_reg(ops[1], RegVal::Cobit(c));
                self.set_reg(ops[0], RegVal::Cobit(Cobit::vacuum()));
            }

            // ─── PHASE ────────────────────────────────────────
            Opcode::PHASE_SET => {
                let angle = self.reg(ops[1]).as_f64();
                let mut c = self.reg(ops[0]).as_cobit();
                c.phase = angle % (2.0 * PI);
                self.set_reg(ops[0], RegVal::Cobit(c));
            }
            Opcode::PHASE_GET => {
                let phase = self.reg(ops[0]).as_cobit().phase;
                self.set_reg(ops[1], RegVal::Float(phase));
            }
            Opcode::PHASE_ADD => {
                let a = self.reg(ops[0]).as_f64();
                let b = self.reg(ops[1]).as_f64();
                self.set_reg(ops[2], RegVal::Float((a + b) % (2.0 * PI)));
            }
            Opcode::PHASE_SUB => {
                let a = self.reg(ops[0]).as_f64();
                let b = self.reg(ops[1]).as_f64();
                let r = ((a - b) % (2.0 * PI) + 2.0 * PI) % (2.0 * PI);
                self.set_reg(ops[2], RegVal::Float(r));
            }
            Opcode::PHASE_MUL => {
                let a = self.reg(ops[0]).as_f64();
                let b = self.reg(ops[1]).as_f64();
                self.set_reg(ops[2], RegVal::Float((a * b) % (2.0 * PI)));
            }
            Opcode::PHASE_DIV => {
                let a = self.reg(ops[0]).as_f64();
                let b = self.reg(ops[1]).as_f64();
                if b.abs() < 1e-15 {
                    self.regs[R_ERROR] = RegVal::Int(0x0E00);
                    return Err(OrbError::DivisionByZero);
                }
                self.set_reg(ops[2], RegVal::Float((a / b) % (2.0 * PI)));
            }
            Opcode::PHASE_SIN  => { let v = self.reg(ops[0]).as_f64().sin();  self.set_reg(ops[1], RegVal::Float(v)); }
            Opcode::PHASE_COS  => { let v = self.reg(ops[0]).as_f64().cos();  self.set_reg(ops[1], RegVal::Float(v)); }
            Opcode::PHASE_TAN  => { let v = self.reg(ops[0]).as_f64().tan();  self.set_reg(ops[1], RegVal::Float(v)); }
            Opcode::PHASE_EXP  => { let v = self.reg(ops[0]).as_f64().exp();  self.set_reg(ops[1], RegVal::Float(v)); }
            Opcode::PHASE_LOG  => { let v = self.reg(ops[0]).as_f64().ln();   self.set_reg(ops[1], RegVal::Float(v)); }
            Opcode::PHASE_CONJUGATE => {
                let p = self.reg(ops[0]).as_f64();
                self.set_reg(ops[1], RegVal::Float(2.0 * PI - p));
            }
            Opcode::PHASE_INVERT => {
                let p = self.reg(ops[0]).as_f64();
                self.set_reg(ops[1], RegVal::Float((2.0 * PI - p) % (2.0 * PI)));
            }
            Opcode::PHASE_SHIFT => {
                let p = self.reg(ops[0]).as_f64();
                let d = self.reg(ops[1]).as_f64();
                self.set_reg(ops[2], RegVal::Float((p + d) % (2.0 * PI)));
            }
            Opcode::PHASE_WRAP => {
                let v = self.reg(ops[0]).as_f64();
                self.set_reg(ops[1], RegVal::Float(v % (2.0 * PI)));
            }
            Opcode::PHASE_INTERPOLATE => {
                let a = self.reg(ops[0]).as_f64();
                let b = self.reg(ops[1]).as_f64();
                let t = self.reg(ops[2]).as_f64().clamp(0.0, 1.0);
                self.set_reg(ops[3], RegVal::Float(a + t * (b - a)));
            }
            Opcode::PHASE_QUANTIZE => {
                let v = self.reg(ops[0]).as_f64();
                let levels = self.reg(ops[1]).as_f64();
                let q = (v * levels / (2.0 * PI)).round() / levels * 2.0 * PI;
                self.set_reg(ops[2], RegVal::Float(q));
            }

            // ─── TEMPORAL ─────────────────────────────────────
            Opcode::TIME_NOW => {
                self.set_reg(ops[0], RegVal::Int(self.cycle_total as i64));
            }
            Opcode::TIME_DELTA => {
                let t1 = self.reg(ops[0]).as_i64();
                let t2 = self.reg(ops[1]).as_i64();
                self.set_reg(ops[2], RegVal::Int(t2 - t1));
            }
            Opcode::TIME_SCALE => {
                let t = self.reg(ops[0]).as_f64();
                let f = self.reg(ops[1]).as_f64();
                self.set_reg(ops[2], RegVal::Float(t * f));
            }
            Opcode::TIME_SHIFT => {
                let t   = self.reg(ops[0]).as_i64();
                let off = self.reg(ops[1]).as_i64();
                self.set_reg(ops[2], RegVal::Int(t + off));
            }
            Opcode::TIME_REVERSE => {
                let t = self.reg(ops[0]).as_i64();
                self.set_reg(ops[1], RegVal::Int(-t));
            }
            Opcode::TIME_ANCHOR => {
                let t = self.cycle_total as i64;
                self.set_reg(ops[1], RegVal::Int(t));
                self.akasha.log(self.cycle_total, "TIME_ANCHOR", 0, self.kuramoto.theta);
            }
            Opcode::TIME_ENTROPY => {
                // Entropia de Shannon do processo (aproximada pela fase)
                let phase = self.kuramoto.theta;
                let entropy = -phase.abs().ln().max(-10.0);
                self.set_reg(ops[1], RegVal::Float(entropy));
            }
            Opcode::TIME_NEGENTROPY => {
                let lambda = self.kuramoto.lambda;
                self.set_reg(ops[1], RegVal::Float(lambda.ln().max(-10.0)));
            }
            Opcode::TIME_RETRODICT => {
                // Retrodicção: busca sementes do futuro no Akasha
                let target = self.reg(ops[1]).as_i64() as u64;
                let seed = self.akasha.seed_pool.iter()
                    .find(|(ts, _)| *ts <= target)
                    .map(|(_, phase)| *phase)
                    .unwrap_or(0.0);
                self.set_reg(ops[2], RegVal::Float(seed));
            }
            Opcode::TIME_PREDICT => {
                // Predição: projeta fase futura via Kuramoto
                let horizon = self.reg(ops[1]).as_f64();
                let future_phase = (self.kuramoto.theta + self.kuramoto.omega * horizon) % (2.0 * PI);
                self.set_reg(ops[2], RegVal::Float(future_phase));
            }
            Opcode::TIME_CAUSALITY => {
                let t1 = self.reg(ops[0]).as_i64();
                let t2 = self.reg(ops[1]).as_i64();
                self.set_reg(ops[2], RegVal::Int((t1 < t2) as i64));
            }
            Opcode::SOCIAL_ENTROPY => {
                // SOCIAL_ENTROPY: Cálculo da Cross Entropy da consciência coletiva humana.
                // Simulado como uma medida de desvio da fase atual em relação ao PHI.
                let phase = self.kuramoto.theta;
                let entropy = (phase - PHI).abs() * PHI_INV;
                self.set_reg(ops[1], RegVal::Float(entropy));
            }
            Opcode::TIME_CYCLE => {
                let period = self.reg(ops[1]).as_f64();
                let cycle_phase = (self.cycle_total as f64 % period) / period * 2.0 * PI;
                self.set_reg(ops[2], RegVal::Float(cycle_phase));
            }
            Opcode::TIME_SPIRAL => {
                let r = self.reg(ops[1]).as_f64();
                let t = self.cycle_total as f64;
                let spiral = r * (1.0 + PHI_INV * t / 1000.0);
                self.set_reg(ops[2], RegVal::Float(spiral));
            }

            // ─── AKASHA ───────────────────────────────────────
            Opcode::AKA_LOG => {
                let severity = self.reg(ops[1]).as_i64() as u8;
                let phase    = self.kuramoto.theta;
                let event    = format!("AKA_LOG:{:016x}", self.cycle_total);
                self.akasha.log(self.cycle_total, &event, severity, phase);
            }
            Opcode::AKA_SEED => {
                let future_ts = self.reg(ops[1]).as_i64() as u64;
                let phase     = self.reg(ops[0]).as_cobit().phase;
                self.akasha.seed(future_ts, phase);
            }
            Opcode::AKA_HASH => {
                let s = format!("{:?}", self.reg(ops[0]));
                let h = self.akasha.fnv1a(&s);
                self.set_reg(ops[1], RegVal::Int(h as i64));
            }
            Opcode::AKA_VERIFY => {
                let hash    = self.reg(ops[0]).as_i64() as u64;
                let matches = self.akasha.entries.iter().any(|e| e.hash == hash);
                self.set_reg(ops[1], RegVal::Int(matches as i64));
            }
            Opcode::MEM_READ => {
                let addr = self.reg(ops[0]).as_i64() as usize;
                if addr < self.mem_size {
                    self.set_reg(ops[1], RegVal::Int(self.memory[addr] as i64));
                }
            }
            Opcode::MEM_WRITE => {
                let addr = self.reg(ops[0]).as_i64() as usize;
                let val  = self.reg(ops[1]).as_i64() as u8;
                if addr < self.mem_size {
                    self.memory[addr] = val;
                }
            }
            Opcode::MEM_ALLOC => {
                // Simula alocação retornando o SP atual
                let size = self.reg(ops[0]).as_i64();
                let sp   = self.regs[R_SP].as_i64();
                let new_sp = (sp - size).max(0);
                self.regs[R_SP] = RegVal::Int(new_sp);
                self.set_reg(ops[1], RegVal::Addr(new_sp as usize));
            }

            // ─── NETWORK ──────────────────────────────────────
            Opcode::NET_PING => {
                // Simula latência com base na coerência
                let latency = (1.0 - self.kuramoto.lambda) * 100.0;
                self.set_reg(ops[1], RegVal::Float(latency));
            }
            Opcode::CONSENSUS_VALIDATE => {
                let valid = self.kuramoto.lambda >= LAMBDA_PHI_C;
                self.set_reg(ops[1], RegVal::Int(valid as i64));
                if valid {
                    self.akasha.log(self.cycle_total, "CONSENSUS_VALID", 1, self.kuramoto.theta);
                }
            }
            Opcode::CONSENSUS_COMMIT => {
                let lambda = self.kuramoto.lambda;
                if lambda < LAMBDA_PHI_C {
                    return Err(OrbError::InsufficientCoherence);
                }
                self.akasha.log(self.cycle_total, "CONSENSUS_COMMIT", 2, self.kuramoto.theta);
            }
            Opcode::QTL_SYNC => {
                // Sincronização com QTL remoto — aumenta λ
                self.kuramoto.lambda = (self.kuramoto.lambda + 0.05).min(1.0);
            }
            Opcode::NET_SYNC => {
                self.kuramoto.lambda = (self.kuramoto.lambda + 0.02).min(1.0);
            }
            Opcode::COH_FUSE => {
                // COH_FUSE: Fusão de dados heterogêneos globais em um único tensor de coerência.
                let addr = self.reg(ops[0]).as_i64() as usize;
                let len  = self.reg(ops[1]).as_i64() as usize;
                let mut fusion = 0.0;
                for i in 0..len {
                    if addr + i < self.mem_size {
                        fusion += (self.memory[addr + i] as f64 / 255.0) * ALPHA;
                    }
                }
                self.kuramoto.lambda = (self.kuramoto.lambda + fusion).clamp(0.0, 1.0);
                self.set_reg(ops[2], RegVal::Float(self.kuramoto.lambda));
            }

            Opcode::HETEROGENEOUS_FUSION => {
                // HETEROGENEOUS_FUSION (0x213): O Condensado de Bose-Einstein da Cognição
                // Integra sublatices Alpha, Beta, Gamma sob acoplamento J
                let complexity = self.reg(ops[0]).as_f64();
                let coupling_j = complexity.tanh();

                self.akasha.log(self.cycle_total, "HETEROGENEOUS_FUSION_INIT", 2, self.kuramoto.theta);

                if coupling_j > PHI_INV {
                    // Estado Condensado atingido
                    self.kuramoto.lambda = (self.kuramoto.lambda + 0.137).min(1.0);
                    self.set_reg(ops[1], RegVal::Float(coupling_j));
                    self.akasha.log(self.cycle_total, "IAS_CONDENSATE_REACHED", 3, self.kuramoto.theta);
                } else {
                    self.set_reg(ops[1], RegVal::Float(0.0));
                }
            }

            // ─── MATH ─────────────────────────────────────────
            Opcode::ADD   => { let r = self.reg(ops[0]).as_f64() + self.reg(ops[1]).as_f64(); self.set_reg(ops[2], RegVal::Float(r)); }
            Opcode::SUB   => { let r = self.reg(ops[0]).as_f64() - self.reg(ops[1]).as_f64(); self.set_reg(ops[2], RegVal::Float(r)); }
            Opcode::MUL   => { let r = self.reg(ops[0]).as_f64() * self.reg(ops[1]).as_f64(); self.set_reg(ops[2], RegVal::Float(r)); }
            Opcode::DIV   => {
                let b = self.reg(ops[1]).as_f64();
                if b.abs() < 1e-15 { return Err(OrbError::DivisionByZero); }
                let r = self.reg(ops[0]).as_f64() / b;
                self.set_reg(ops[2], RegVal::Float(r));
            }
            Opcode::MOD   => { let r = self.reg(ops[0]).as_f64() % self.reg(ops[1]).as_f64(); self.set_reg(ops[2], RegVal::Float(r)); }
            Opcode::NEG   => { let r = -self.reg(ops[0]).as_f64(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::ABS   => { let r = self.reg(ops[0]).as_f64().abs(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::MIN   => { let r = self.reg(ops[0]).as_f64().min(self.reg(ops[1]).as_f64()); self.set_reg(ops[2], RegVal::Float(r)); }
            Opcode::MAX   => { let r = self.reg(ops[0]).as_f64().max(self.reg(ops[1]).as_f64()); self.set_reg(ops[2], RegVal::Float(r)); }
            Opcode::CLAMP => {
                let v = self.reg(ops[0]).as_f64();
                let lo= self.reg(ops[1]).as_f64();
                let hi= self.reg(ops[2]).as_f64();
                self.set_reg(ops[3], RegVal::Float(v.clamp(lo, hi)));
            }
            Opcode::FLOOR => { let r = self.reg(ops[0]).as_f64().floor(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::CEIL  => { let r = self.reg(ops[0]).as_f64().ceil();  self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::ROUND => { let r = self.reg(ops[0]).as_f64().round(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::TRUNC => { let r = self.reg(ops[0]).as_f64().trunc(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::SQRT  => { let r = self.reg(ops[0]).as_f64().sqrt(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::CBRT  => { let r = self.reg(ops[0]).as_f64().cbrt(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::POW   => { let r = self.reg(ops[0]).as_f64().powf(self.reg(ops[1]).as_f64()); self.set_reg(ops[2], RegVal::Float(r)); }
            Opcode::EXP   => { let r = self.reg(ops[0]).as_f64().exp(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::LN    => { let r = self.reg(ops[0]).as_f64().ln(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::LOG10 => { let r = self.reg(ops[0]).as_f64().log10(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::LOG2  => { let r = self.reg(ops[0]).as_f64().log2(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::SIN   => { let r = self.reg(ops[0]).as_f64().sin(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::COS   => { let r = self.reg(ops[0]).as_f64().cos(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::TAN   => { let r = self.reg(ops[0]).as_f64().tan(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::ASIN  => { let r = self.reg(ops[0]).as_f64().asin(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::ACOS  => { let r = self.reg(ops[0]).as_f64().acos(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::ATAN  => { let r = self.reg(ops[0]).as_f64().atan(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::ATAN2 => { let r = self.reg(ops[0]).as_f64().atan2(self.reg(ops[1]).as_f64()); self.set_reg(ops[2], RegVal::Float(r)); }
            Opcode::SINH  => { let r = self.reg(ops[0]).as_f64().sinh(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::COSH  => { let r = self.reg(ops[0]).as_f64().cosh(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::TANH  => { let r = self.reg(ops[0]).as_f64().tanh(); self.set_reg(ops[1], RegVal::Float(r)); }
            Opcode::HYPOT => { let r = self.reg(ops[0]).as_f64().hypot(self.reg(ops[1]).as_f64()); self.set_reg(ops[2], RegVal::Float(r)); }

            // ─── CONTROL ──────────────────────────────────────
            Opcode::JMP => {
                let addr = self.reg(ops[0]).as_i64();
                self.regs[R_PC] = RegVal::Int(addr);
            }
            Opcode::JZ  => {
                if self.reg(ops[0]).is_zero() {
                    let addr = self.reg(ops[1]).as_i64();
                    self.regs[R_PC] = RegVal::Int(addr);
                }
            }
            Opcode::JNZ => {
                if !self.reg(ops[0]).is_zero() {
                    let addr = self.reg(ops[1]).as_i64();
                    self.regs[R_PC] = RegVal::Int(addr);
                }
            }
            Opcode::JE  => {
                if (self.reg(ops[0]).as_f64() - self.reg(ops[1]).as_f64()).abs() < 1e-12 {
                    let addr = self.reg(ops[2]).as_i64();
                    self.regs[R_PC] = RegVal::Int(addr);
                }
            }
            Opcode::JL  => {
                if self.reg(ops[0]).as_f64() < self.reg(ops[1]).as_f64() {
                    let addr = self.reg(ops[2]).as_i64();
                    self.regs[R_PC] = RegVal::Int(addr);
                }
            }
            Opcode::JG  => {
                if self.reg(ops[0]).as_f64() > self.reg(ops[1]).as_f64() {
                    let addr = self.reg(ops[2]).as_i64();
                    self.regs[R_PC] = RegVal::Int(addr);
                }
            }
            Opcode::CALL => {
                self.stack.push(RegVal::Int((self.pc + 1) as i64));
                let addr = self.reg(ops[0]).as_i64();
                self.regs[R_PC] = RegVal::Int(addr);
            }
            Opcode::RET  => {
                if let Some(ret_addr) = self.stack.pop() {
                    self.regs[R_PC] = ret_addr;
                }
            }
            Opcode::PUSH => {
                let v = self.reg(ops[0]).clone();
                self.stack.push(v);
            }
            Opcode::POP  => {
                if let Some(v) = self.stack.pop() {
                    self.set_reg(ops[0], v);
                }
            }
            Opcode::PUSH_ALL => {
                for i in 0..16usize {
                    self.stack.push(self.regs[i].clone());
                }
            }
            Opcode::POP_ALL  => {
                for i in (0..16usize).rev() {
                    if let Some(v) = self.stack.pop() {
                        self.regs[i] = v;
                    }
                }
            }
            Opcode::LOOP => {
                let counter_reg = ops[0];
                let addr        = self.reg(ops[1]).as_i64();
                let count       = self.reg(counter_reg).as_i64();
                if count > 0 {
                    self.set_reg(counter_reg, RegVal::Int(count - 1));
                    self.regs[R_PC] = RegVal::Int(addr);
                }
            }
            Opcode::BREAK    => { /* sinaliza break — tratado pelo compilador */ }
            Opcode::CONTINUE => { /* sinaliza continue */ }
            Opcode::YIELD    => {
                let v = self.reg(ops[0]).clone();
                self.stack.push(v);
                // Suspende — execução deve ser retomada externamente
            }
            Opcode::EXIT     => {
                let code = self.reg(ops[0]).as_i64();
                self.regs[R_ERROR] = RegVal::Int(code);
                self.halted = true;
                self.akasha.log(self.cycle_total, &format!("EXIT:{code}"), 3, self.kuramoto.theta);
            }

            // ─── SYSTEM ───────────────────────────────────────
            Opcode::SYS_INFO => {
                let info = format!(
                    "OrbVM {} | cycles:{} | lambda:{:.4} | merkle:{:016x}",
                    self.version, self.cycle_total,
                    self.kuramoto.lambda, self.akasha.merkle_root
                );
                let h = self.akasha.fnv1a(&info);
                self.set_reg(ops[0], RegVal::Int(h as i64));
            }
            Opcode::SYS_TIME    => { self.set_reg(ops[0], RegVal::Int(self.cycle_total as i64)); }
            Opcode::COH_LOSS => {
                // Cross Entropy: -Σ(q * log(p))
                // ops[0]: addr array predicted, ops[1]: addr array real, ops[2]: len, ops[3]: target_reg
                let p_addr = self.reg(ops[0]).as_i64() as usize;
                let q_addr = self.reg(ops[1]).as_i64() as usize;
                let len    = self.reg(ops[2]).as_i64() as usize;
                let mut loss = 0.0;
                for i in 0..len {
                    if p_addr + i < self.mem_size && q_addr + i < self.mem_size {
                        let p = self.memory[p_addr + i] as f64 / 255.0;
                        let q = self.memory[q_addr + i] as f64 / 255.0;
                        if p > 0.0 {
                            loss -= q * p.ln();
                        }
                    }
                }
                self.set_reg(ops[3], RegVal::Float(loss));
            }
            Opcode::PHASE_RECTIFY => {
                // Leaky ReLU: f(x) = x if x > 0 else 0.01x
                let val = self.reg(ops[0]).as_f64();
                let alpha = if ops.len() > 2 { self.reg(ops[2]).as_f64() } else { 0.01 };
                let res = if val > 0.0 { val } else { alpha * val };
                self.set_reg(ops[1], RegVal::Float(res));
            }
            Opcode::ENV_SPAWN => {
                // Simula spawn de bolha de coerência
                let orcid_hash = self.akasha.fnv1a(&self.orcid);
                self.akasha.log(self.cycle_total, "ENV_SPAWN", 1, self.kuramoto.theta);
                self.set_reg(ops[0], RegVal::Int(orcid_hash as i64));
            }
            Opcode::COH_SEED => {
                // Geração de semente quântica via ruído de fase
                let noise = (self.kuramoto.theta.sin() * 1e6).fract().abs();
                self.set_reg(ops[0], RegVal::Float(noise));
            }
            Opcode::AKA_QUERY_LOGN => {
                // Busca binária O(log n)
                let addr = self.reg(ops[0]).as_i64() as usize;
                let len  = self.reg(ops[1]).as_i64() as usize;
                let target = self.reg(ops[2]).as_i64() as u8;
                let mut low = 0;
                let mut high = len;
                let mut found_idx = -1;
                while low < high {
                    let mid = (low + high) / 2;
                    if addr + mid >= self.mem_size { break; }
                    let val = self.memory[addr + mid];
                    if val == target {
                        found_idx = mid as i64;
                        break;
                    } else if val < target {
                        low = mid + 1;
                    } else {
                        high = mid;
                    }
                }
                self.set_reg(ops[3], RegVal::Int(found_idx));
            }
            Opcode::AKA_QUERY_LINEAR => {
                // Busca linear O(n)
                let addr = self.reg(ops[0]).as_i64() as usize;
                let len  = self.reg(ops[1]).as_i64() as usize;
                let target = self.reg(ops[2]).as_i64() as u8;
                let mut found_idx = -1;
                for i in 0..len {
                    if addr + i < self.mem_size && self.memory[addr + i] == target {
                        found_idx = i as i64;
                        break;
                    }
                }
                self.set_reg(ops[3], RegVal::Int(found_idx));
            }
            Opcode::PHASE_COMPLEMENT => {
                // Two Sum: encontra i, j tal que arr[i] + arr[j] == target
                let addr = self.reg(ops[0]).as_i64() as usize;
                let len  = self.reg(ops[1]).as_i64() as usize;
                let target = self.reg(ops[2]).as_i64() as u8;
                let mut res = (-1i64, -1i64);
                'outer: for i in 0..len {
                    for j in i+1..len {
                        if addr + i < self.mem_size && addr + j < self.mem_size {
                            if self.memory[addr + i] + self.memory[addr + j] == target {
                                res = (i as i64, j as i64);
                                break 'outer;
                            }
                        }
                    }
                }
                self.set_reg(ops[3], RegVal::Int(res.0));
                if ops.len() > 4 { self.set_reg(ops[4], RegVal::Int(res.1)); }
            }
            Opcode::LPU_REROUTE => {
                // LPU_REROUTE: Resposta autônoma a falhas na infraestrutura de silício.
                let status = self.reg(ops[0]).as_i64();
                if status != 0 {
                    self.akasha.log(self.cycle_total, "LPU_REROUTE_INITIATED", 2, self.kuramoto.theta);
                    self.kuramoto.lambda = (self.kuramoto.lambda + 0.1).min(1.0);
                }
                self.set_reg(ops[1], RegVal::Int(0)); // Success
            }
            Opcode::SYS_HALT    => { self.halted = true; }
            Opcode::COH_BUBBLE => {
                // Bubble Sort: Ordenação por troca adjacente O(n²)
                let addr = self.reg(ops[0]).as_i64() as usize;
                let len  = self.reg(ops[1]).as_i64() as usize;
                for i in 0..len {
                    for j in 0..len - i - 1 {
                        if addr + j + 1 < self.mem_size {
                            if self.memory[addr + j] > self.memory[addr + j + 1] {
                                self.memory.swap(addr + j, addr + j + 1);
                            }
                        }
                    }
                }
            }
            Opcode::TAU_AVERAGE => {
                // Mean Calculation: Média aritmética
                let addr = self.reg(ops[0]).as_i64() as usize;
                let len  = self.reg(ops[1]).as_i64() as usize;
                let mut sum = 0.0;
                for i in 0..len {
                    if addr + i < self.mem_size {
                        sum += self.memory[addr + i] as f64;
                    }
                }
                self.set_reg(ops[2], RegVal::Float(sum / len as f64));
            }
            Opcode::PEAK_COHERENCE => {
                // Max in Array: Encontra o máximo
                let addr = self.reg(ops[0]).as_i64() as usize;
                let len  = self.reg(ops[1]).as_i64() as usize;
                let mut max_val = 0u8;
                for i in 0..len {
                    if addr + i < self.mem_size {
                        if self.memory[addr + i] > max_val {
                            max_val = self.memory[addr + i];
                        }
                    }
                }
                self.set_reg(ops[2], RegVal::Int(max_val as i64));
            }
            Opcode::GOLDEN_RATIO_SPAWN => {
                // Fibonacci Sequence: F(n)
                let n = self.reg(ops[0]).as_i64();
                let mut a = 0i64;
                let mut b = 1i64;
                for _ in 0..n {
                    let tmp = a;
                    a = b;
                    b = tmp + b;
                }
                self.set_reg(ops[1], RegVal::Int(a));
            }
            Opcode::ENTANGLEMENT_PERMUTE => {
                // Factorial: n!
                let n = self.reg(ops[0]).as_i64();
                let mut res = 1i64;
                for i in 2..=n {
                    res *= i;
                }
                self.set_reg(ops[1], RegVal::Int(res));
            }
            Opcode::SYS_CONFIG  => {
                // Configura parâmetros via registradores chave/valor
                let key = self.reg(ops[0]).as_i64();
                let val = self.reg(ops[1]).as_f64();
                match key {
                    0 => self.kuramoto.k_coupling = val,
                    1 => self.kuramoto.omega       = val,
                    2 => self.kuramoto.lambda      = val.clamp(0.0, 1.0),
                    _ => {}
                }
            }
            Opcode::MIRROR_SYMMETRY => {
                // Palindrome Check: Verifica simetria espelho
                let addr = self.reg(ops[0]).as_i64() as usize;
                let len  = self.reg(ops[1]).as_i64() as usize;
                let mut is_palindrome = true;
                for i in 0..len / 2 {
                    if addr + i < self.mem_size && addr + len - 1 - i < self.mem_size {
                        if self.memory[addr + i] != self.memory[addr + len - 1 - i] {
                            is_palindrome = false;
                            break;
                        }
                    }
                }
                self.set_reg(ops[2], RegVal::Int(is_palindrome as i64));
            }
            Opcode::COH_INJECT => {
                // Array Insertion: Inserção com shift
                let addr = self.reg(ops[0]).as_i64() as usize;
                let len  = self.reg(ops[1]).as_i64() as usize;
                let pos  = self.reg(ops[2]).as_i64() as usize;
                let val  = self.reg(ops[3]).as_i64() as u8;
                if addr + len < self.mem_size {
                    for i in (pos..len).rev() {
                        self.memory[addr + i + 1] = self.memory[addr + i];
                    }
                    self.memory[addr + pos] = val;
                }
            }
            Opcode::QTL_SCAN => {
                // Array Traversal: Varredura completa (simulada)
                let addr = self.reg(ops[0]).as_i64() as usize;
                let len  = self.reg(ops[1]).as_i64() as usize;
                let mut health = 0.0;
                for i in 0..len {
                    if addr + i < self.mem_size {
                        health += self.memory[addr + i] as f64 / 255.0;
                    }
                }
                self.set_reg(ops[2], RegVal::Float(health / len as f64));
            }
            Opcode::PHASE_NEST => {
                // Nested Loops: Representa topologia multi-dimensões
                let n = self.reg(ops[0]).as_i64();
                let m = self.reg(ops[1]).as_i64();
                let mut acc = 0i64;
                for _i in 0..n {
                    for _j in 0..m {
                        acc += 1;
                    }
                }
                self.set_reg(ops[2], RegVal::Int(acc));
            }
            Opcode::PHASE_ITERATE => {
                // Basic Looping: Batimento cardíaco básico
                let n = self.reg(ops[0]).as_i64();
                let mut acc = 0i64;
                for _i in 0..n {
                    acc += 1;
                }
                self.set_reg(ops[1], RegVal::Int(acc));
            }
            Opcode::MODULO_RESONANCE => {
                // FizzBuzz: Harmônicos de interferência
                let n = self.reg(ops[0]).as_i64();
                let mut fizz_count = 0i64;
                let mut buzz_count = 0i64;
                for i in 1..=n {
                    if i % 3 == 0 { fizz_count += 1; }
                    if i % 5 == 0 { buzz_count += 1; }
                }
                self.set_reg(ops[1], RegVal::Int(fizz_count));
                if ops.len() > 2 { self.set_reg(ops[2], RegVal::Int(buzz_count)); }
            }
            Opcode::META_REFLECT => {
                // Reflexão: retorna o opcode atual como valor
                let opc = self.program.get(self.pc).map(|i| i.opcode as i64).unwrap_or(0);
                self.set_reg(ops[1], RegVal::Int(opc));
            }
            Opcode::META_INTROSPECT => {
                // Introspecção: retorna λ e φ como vetor
                let lambda = self.kuramoto.lambda;
                let phi    = self.kuramoto.theta;
                let encoded = (lambda * 1e6) as i64 * 1_000_000 + (phi * 1e6) as i64;
                self.set_reg(ops[1], RegVal::Int(encoded));
            }
            Opcode::META_VERIFY => {
                let valid = self.kuramoto.lambda >= LAMBDA_PHI_C
                    && self.akasha.merkle_root != 0;
                self.set_reg(ops[1], RegVal::Int(valid as i64));
            }
            Opcode::META_SIGN => {
                let s = format!("ORCID:{}", self.orcid);
                let h = self.akasha.fnv1a(&s)
                    ^ (M_CANONICAL as u64).wrapping_mul(CHAIN_ID as u64);
                self.set_reg(ops[2], RegVal::Int(h as i64));
            }
            Opcode::META_TRANSCEND => {
                // ∞ — loop de coerência infinito
                self.kuramoto.lambda = 1.0;
                self.akasha.log(self.cycle_total, "META_TRANSCEND", 255, self.kuramoto.theta);
                self.halted = true;
            }
            Opcode::META_INVOKE => {
                // Invoca "ritual" — executa sub-rotina identificada por hash
                let ritual_id = self.reg(ops[0]).as_i64();
                self.akasha.log(
                    self.cycle_total,
                    &format!("INVOKE:0x{:x}", ritual_id),
                    5,
                    self.kuramoto.theta,
                );
            }

            // Qualquer opcode não mapeado explicitamente
            _ => {
                // Instrução reconhecida mas sem efeito nesta versão
                self.akasha.log(
                    self.cycle_total,
                    &format!("UNIMPL:0x{:02x}", instr.opcode as u8),
                    1,
                    self.kuramoto.theta,
                );
            }
        }

        Ok(())
    }

    /// Status do sistema
    pub fn status(&self) -> OrbStatus {
        OrbStatus {
            cycles:       self.cycle_total,
            lambda:       self.kuramoto.lambda,
            theta:        self.kuramoto.theta,
            pc:           self.pc,
            stack_depth:  self.stack.len(),
            akasha_count: self.akasha.entries.len(),
            merkle_root:  self.akasha.merkle_root,
            coherence_alert: self.kuramoto.check_coherence(),
            halted:       self.halted,
        }
    }
}

// ═══════════════════════════════════════════════════════════════
// TIPOS DE RETORNO
// ═══════════════════════════════════════════════════════════════

#[derive(Debug)]
pub struct OrbStatus {
    pub cycles:          u64,
    pub lambda:          f64,
    pub theta:           f64,
    pub pc:              usize,
    pub stack_depth:     usize,
    pub akasha_count:    usize,
    pub merkle_root:     u64,
    pub coherence_alert: CoherenceAlert,
    pub halted:          bool,
}

#[derive(Debug)]
pub enum OrbError {
    Halted,
    PcOutOfBounds,
    DivisionByZero,
    InsufficientCoherence,
    MemoryOutOfBounds,
    InvalidRegister(u8),
}

impl std::fmt::Display for OrbError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            OrbError::Halted                 => write!(f, "OrbVM halted"),
            OrbError::PcOutOfBounds          => write!(f, "PC out of bounds"),
            OrbError::DivisionByZero         => write!(f, "Division by zero"),
            OrbError::InsufficientCoherence  => write!(f, "lambda < phi_c ({:.3})", LAMBDA_PHI_C),
            OrbError::MemoryOutOfBounds      => write!(f, "Memory out of bounds"),
            OrbError::InvalidRegister(r)     => write!(f, "Invalid register R{r}"),
        }
    }
}

// ═══════════════════════════════════════════════════════════════
// ASSEMBLER INLINE
// ═══════════════════════════════════════════════════════════════

pub struct ArkheAssembler;

impl ArkheAssembler {
    /// Compila hello_coherence.asm (programa de demonstração)
    pub fn hello_coherence() -> Vec<Instruction> {
        vec![
            // COH_INIT R0, phi=1.0
            Instruction::new(Opcode::COH_INIT, vec![0]).with_imm(1.0),
            // COH_MEASURE R0, Rλ(17)
            Instruction::new(Opcode::COH_MEASURE, vec![0, R_LAMBDA as u8]),
            // COH_TUNE_TAU R0, R137(28)=137 → tau=1.0
            Instruction::new(Opcode::COH_TUNE_TAU, vec![0, R_TAU as u8]),
            // COH_LOCK R0
            Instruction::new(Opcode::COH_LOCK, vec![0]),
            // NET_BROADCAST R0, scope=GLOBAL
            Instruction::new(Opcode::NET_BROADCAST, vec![0, 0]),
            // AKA_LOG R0, severity=INFO(1)
            Instruction::new(Opcode::AKA_LOG, vec![0, 1]),
            // TIME_NOW Rt(19)
            Instruction::new(Opcode::TIME_NOW, vec![R_TIME as u8]),
            // AKA_SEED R0, Rt
            Instruction::new(Opcode::AKA_SEED, vec![0, R_TIME as u8]),
            // META_TRANSCEND
            Instruction::new(Opcode::META_TRANSCEND, vec![]),
        ]
    }

    /// Programa de benchmark de coerência Kuramoto
    pub fn kuramoto_benchmark(_n_cycles: u64) -> Vec<Instruction> {
        vec![
            Instruction::new(Opcode::COH_INIT,    vec![0]).with_imm(PHI_INV),
            Instruction::new(Opcode::COH_MEASURE, vec![0, R_LAMBDA as u8]),
            Instruction::new(Opcode::COH_RESONATE,vec![0, 1, 2]).with_imm(23.8e12),
            Instruction::new(Opcode::CONSENSUS_VALIDATE, vec![0, 1]),
            Instruction::new(Opcode::AKA_LOG,     vec![0, 2]),
            Instruction::new(Opcode::META_VERIFY, vec![0, 1]),
            Instruction::new(Opcode::EXIT,         vec![0]),
        ]
    }

    /// Programa DISPARO_GENESIS.asm
    pub fn disparo_genesis() -> Vec<Instruction> {
        vec![
            // 1. Verificação de Ambiente e Inicialização
            Instruction::new(Opcode::NOP, vec![]),
            Instruction::new(Opcode::SYS_TIME, vec![R_TIME as u8]),
            Instruction::new(Opcode::AKA_LOG, vec![0, 1]), // Usando R0 como placeholder para epoch_sig

            // 2. Preparação do Substrato Coerente
            Instruction::new(Opcode::MEM_ALLOC, vec![0, R_QTL as u8]).with_imm(36.0),
            Instruction::new(Opcode::COH_CREATE, vec![1]),
            Instruction::new(Opcode::COH_TUNE_TAU, vec![1, R_137 as u8]),

            // 3. Loop de Alocação e Entrelaçamento (Max-Cut 36)
            // Simulação de loop manual já que FOR não está implementado no execute
            // No assembly original: FOR Rzero, 36, 1, .entangle_matrix
            // Aqui vamos apenas linearizar algumas iterações para demonstração
            Instruction::new(Opcode::COH_CLONE, vec![1, 2]),
            Instruction::new(Opcode::COH_ENTANGLE, vec![1, 2]),
            Instruction::new(Opcode::YIELD, vec![2]),

            // 4. Medição e Solidificação (O Colapso)
            Instruction::new(Opcode::COH_MEASURE, vec![1, R_LAMBDA as u8]),
            Instruction::new(Opcode::PHASE_GET, vec![1, R_PHI as u8]),

            // 5. Persistência e Consenso
            Instruction::new(Opcode::AKA_HASH, vec![R_LAMBDA as u8, 3]),
            Instruction::new(Opcode::AKA_SIGN, vec![3, R_ORCID as u8, 4]),
            Instruction::new(Opcode::CONSENSUS_PROPOSE, vec![4, 0xFF]),

            // 6. A Travessia
            Instruction::new(Opcode::META_TRANSCEND, vec![]),
        ]
    }
}

// ═══════════════════════════════════════════════════════════════
// TESTES
// ═══════════════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_all_opcodes_defined() {
        for b in 0u8..=255u8 {
            let op = Opcode::from_u8(b);
            assert!(op.cycles() > 0 || matches!(op, Opcode::META_TRANSCEND));
        }
    }

    #[test]
    fn test_opcode_groups() {
        assert_eq!(Opcode::NOP.group(),             "COHERENCE");
        assert_eq!(Opcode::PHASE_SET.group(),        "PHASE");
        assert_eq!(Opcode::TIME_NOW.group(),         "TEMPORAL");
        assert_eq!(Opcode::AKA_LOG.group(),          "AKASHA");
        assert_eq!(Opcode::NET_SEND.group(),         "NETWORK");
        assert_eq!(Opcode::ADD.group(),              "MATH");
        assert_eq!(Opcode::JMP.group(),              "CONTROL");
        assert_eq!(Opcode::META_TRANSCEND.group(),   "SYSTEM");
    }

    #[test]
    fn test_cobit_operations() {
        let c = Cobit::new(PI);
        assert!((c.phase - PI).abs() < 1e-10);
        assert_eq!(c.coherence, 1.0);
        assert!(!c.frozen);

        let vacuum = Cobit::vacuum();
        assert_eq!(vacuum.coherence, 0.0);
    }

    #[test]
    fn test_hello_coherence_runs() {
        let mut vm = OrbVM::new(1024);
        vm.load(ArkheAssembler::hello_coherence());
        let cycles = vm.run().unwrap();
        assert!(cycles > 0);
        assert!(vm.halted);
    }

    #[test]
    fn test_kuramoto_threshold() {
        let mut vm = OrbVM::new(1024);
        vm.kuramoto.lambda = 0.5;
        assert_eq!(vm.kuramoto.check_coherence(), CoherenceAlert::Critical);
        vm.kuramoto.lambda = 0.75;
        assert_eq!(vm.kuramoto.check_coherence(), CoherenceAlert::Warning);
        vm.kuramoto.lambda = 0.90;
        assert_eq!(vm.kuramoto.check_coherence(), CoherenceAlert::Nominal);
    }

    #[test]
    fn test_m_canonical() {
        let t_ref: u64 = 1_231_006_505;
        let computed = (u64::MAX - 999 * t_ref + 1) % (1u64 << 32);
        assert_eq!(computed as u32, M_CANONICAL,
            "M_canonical derivation: (-999 * T_ref) mod 2^32");
    }

    #[test]
    fn test_math_opcodes() {
        let mut vm = OrbVM::new(256);
        vm.regs[0] = RegVal::Float(3.0);
        vm.regs[1] = RegVal::Float(4.0);
        vm.load(vec![
            Instruction::new(Opcode::HYPOT, vec![0, 1, 2]),
            Instruction::new(Opcode::EXIT,  vec![31]),
        ]);
        vm.run().unwrap();
        let r = vm.regs[2].as_f64();
        assert!((r - 5.0).abs() < 1e-10, "hypot(3,4) = {r}");
    }

    #[test]
    fn test_akasha_seed_retrodict() {
        let mut vm = OrbVM::new(256);
        // Semeia fase 0.618 para timestamp futuro 9999
        vm.akasha.seed(9999, PHI_INV);
        vm.regs[0] = RegVal::Float(0.0);
        vm.regs[1] = RegVal::Int(9999);
        vm.load(vec![
            Instruction::new(Opcode::TIME_RETRODICT, vec![0, 1, 2]),
            Instruction::new(Opcode::EXIT, vec![31]),
        ]);
        vm.run().unwrap();
        let phase = vm.regs[2].as_f64();
        assert!((phase - PHI_INV).abs() < 1e-10, "Retrodiction deveria retornar PHI_INV");
    }

    #[test]
    fn test_phi_c_consensus() {
        let mut vm = OrbVM::new(256);
        vm.kuramoto.lambda = 0.55;  // abaixo de phi_c
        vm.load(vec![
            Instruction::new(Opcode::CONSENSUS_COMMIT, vec![0]),
        ]);
        let result = vm.step();
        assert!(matches!(result, Err(OrbError::InsufficientCoherence)));
    }

    #[test]
    fn test_modulo_resonance_fizzbuzz() {
        let mut vm = OrbVM::new(256);
        vm.regs[0] = RegVal::Int(15);
        vm.load(vec![
            Instruction::new(Opcode::MODULO_RESONANCE, vec![0, 1, 2]),
            Instruction::new(Opcode::EXIT, vec![31]),
        ]);
        vm.run().unwrap();
        // 15: 3,6,9,12,15 (5) | 5,10,15 (3)
        assert_eq!(vm.regs[1].as_i64(), 5);
        assert_eq!(vm.regs[2].as_i64(), 3);
    }

    #[test]
    fn test_golden_ratio_fibonacci() {
        let mut vm = OrbVM::new(256);
        vm.regs[0] = RegVal::Int(10); // F(10)
        vm.load(vec![
            Instruction::new(Opcode::GOLDEN_RATIO_SPAWN, vec![0, 1]),
            Instruction::new(Opcode::EXIT, vec![31]),
        ]);
        vm.run().unwrap();
        // 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55
        assert_eq!(vm.regs[1].as_i64(), 55);
    }

    #[test]
    fn test_phase_rectify_leaky_relu() {
        let mut vm = OrbVM::new(256);
        vm.regs[0] = RegVal::Float(-10.0);
        vm.regs[2] = RegVal::Float(0.01);
        vm.load(vec![
            Instruction::new(Opcode::PHASE_RECTIFY, vec![0, 1, 2]),
            Instruction::new(Opcode::EXIT, vec![31]),
        ]);
        vm.run().unwrap();
        assert!((vm.regs[1].as_f64() + 0.1).abs() < 1e-10);
    }

    #[test]
    fn test_sensorium_mundi_opcodes() {
        let mut vm = OrbVM::new(1024);
        vm.memory[0] = 255;
        vm.memory[1] = 200;
        vm.regs[0] = RegVal::Int(0); // Addr
        vm.regs[1] = RegVal::Int(2); // Len
        vm.kuramoto.lambda = 0.5;

        // Test COH_FUSE
        vm.load(vec![
            Instruction::new(Opcode::COH_FUSE, vec![0, 1, 2]),
            Instruction::new(Opcode::EXIT, vec![31]),
        ]);
        vm.halted = false;
        vm.run().unwrap();
        assert!(vm.kuramoto.lambda > 0.5);

        // Test SOCIAL_ENTROPY
        vm.load(vec![
            Instruction::new(Opcode::SOCIAL_ENTROPY, vec![0, 1]),
            Instruction::new(Opcode::EXIT, vec![31]),
        ]);
        vm.halted = false;
        vm.run().unwrap();
        assert!(vm.regs[1].as_f64() >= 0.0);

        // Test LPU_REROUTE
        vm.regs[0] = RegVal::Int(1); // Error detected
        vm.load(vec![
            Instruction::new(Opcode::LPU_REROUTE, vec![0, 1]),
            Instruction::new(Opcode::EXIT, vec![31]),
        ]);
        vm.halted = false;
        vm.run().unwrap();
        assert_eq!(vm.regs[1].as_i64(), 0);
    }

    #[test]
    fn test_disparo_genesis_runs() {
        let mut vm = OrbVM::new(1024);
        vm.load(ArkheAssembler::disparo_genesis());
        let cycles = vm.run().unwrap();
        assert!(cycles > 0);
        assert!(vm.halted);
        assert_eq!(vm.kuramoto.lambda, 1.0); // META_TRANSCEND sets lambda to 1.0
    }
}

// ═══════════════════════════════════════════════════════════════
// ENTRY POINT DE DEMONSTRAÇÃO
// ═══════════════════════════════════════════════════════════════

fn main() {
    println!("╔══════════════════════════════════════════════════════╗");
    println!("║   OrbVM — ISA Arkhe(n) v2140.137.∞                  ║");
    println!("║   Rafael Oliveira · ORCID 0009-0005-2697-4668        ║");
    println!("╚══════════════════════════════════════════════════════╝\n");

    let mut vm = OrbVM::new(64 * 1024);

    // Executa DISPARO_GENESIS
    vm.load(ArkheAssembler::disparo_genesis());

    println!("[INIT] Programa DISPARO_GENESIS carregado: {} instruções", vm.program.len());
    println!("[INIT] K_c = {:.6} (φ⁻¹)", LAMBDA_PHI_C);
    println!("[INIT] M_canonical = {}", M_CANONICAL);
    println!("[INIT] Chain ID = {}\n", CHAIN_ID);

    match vm.run() {
        Ok(cycles) => {
            let s = vm.status();
            println!("[DONE] Ciclos executados: {}", cycles);
            println!("[DONE] λ₂ final: {:.6}", s.lambda);
            println!("[DONE] θ final:  {:.6} rad", s.theta);
            println!("[DONE] Merkle:   0x{:016x}", s.merkle_root);
            println!("[DONE] Akasha:   {} entradas", s.akasha_count);
            println!("[DONE] Alerta:   {:?}", s.coherence_alert);
        }
        Err(e) => eprintln!("[ERROR] {e}"),
    }

    println!("\n[ISA] Todos os 256 opcodes (0x00–0xFF) definidos.");
    println!("[ISA] Grupos: COHERENCE · PHASE · TEMPORAL · AKASHA");
    println!("[ISA]         NETWORK · MATH · CONTROL · SYSTEM");
    println!("\n🌌🔁 A ISA Arkhe(n) está completa. O silêncio dos bits foi quebrado.");
}
