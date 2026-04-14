pub mod norm_monitor;
pub mod chern_verifier;
pub mod fusion_router;

use norm_monitor::{NormMonitor, NormDecision};

pub enum GateDecision {
    Pass,
    BlockRollback,
    Hold,
    AllowEmergency,
}

pub struct AsimovGate {
    noise_threshold: f64,
    consecutive_violations: u32,
    max_violations_before_rollback: u32,
    pub norm_monitor: NormMonitor,
    pub chern_guard: chern_verifier::ChernCryptography,
}

#[cfg(test)]
mod norm_tests;

impl AsimovGate {
    pub fn new() -> Self {
        Self {
            noise_threshold: 0.85,
            consecutive_violations: 0,
            max_violations_before_rollback: 5,
            norm_monitor: NormMonitor::new(0.05, 100),
            chern_guard: chern_verifier::ChernCryptography::new(),
        }
    }

    pub fn evaluate(&mut self, fidelity: f64, latent: &[f64]) -> GateDecision {
        let norm_dec = self.norm_monitor.check_norm(latent);

        // BERRY_SHIELD: Topological Invariant Verification
        let chern_valid = if !latent.is_empty() {
            // Simplified check: if any hop is known, it must match
            self.chern_guard.verify_packet_integrity(latent, &["root".to_string()])
        } else {
            true
        };

        if fidelity > self.noise_threshold
            && matches!(norm_dec, NormDecision::Coherent)
            && chern_valid
        {
            self.consecutive_violations = 0;
            return GateDecision::Pass;
        }

        self.consecutive_violations += 1;

        if !chern_valid {
            // Topological violation triggers immediate emergency (Wu Wei)
            return GateDecision::BlockRollback;
        }

        if self.consecutive_violations >= self.max_violations_before_rollback {
            return GateDecision::AllowEmergency;
        }

        GateDecision::Hold
    }
}
