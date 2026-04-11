pub mod norm_monitor;

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
    pub lucid_mode: bool,
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
            lucid_mode: true,
        }
    }

    pub fn evaluate(&mut self, fidelity: f64, latent: &[f64]) -> GateDecision {
        let norm_dec = self.norm_monitor.check_norm(latent);

        if fidelity > self.noise_threshold && matches!(norm_dec, NormDecision::Coherent) {
            self.consecutive_violations = 0;
            return GateDecision::Pass;
        }

        self.consecutive_violations += 1;

        if self.consecutive_violations >= self.max_violations_before_rollback {
            return GateDecision::AllowEmergency;
        }

        GateDecision::Hold
    }
}
