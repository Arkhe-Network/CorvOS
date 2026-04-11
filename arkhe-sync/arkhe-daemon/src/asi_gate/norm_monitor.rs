pub enum NormDecision {
    Coherent,
    Unstable,
    DivergingHigh,
    DivergingLow,
}

pub enum NMSIDecision {
    Coherent,
    DecoherenceDetected,
}

pub struct NormMonitor {
    norm_threshold: f64,
    history: Vec<f64>,
    coherence_window: usize,
    nmsi_tolerance: f64,
    pub lucidity_depth: f64, // δ: 0 to 1
}

const BETA_NMSI: f64 = 1.25e-3;
const OSC_CONST: f64 = 1.267;
const LAMBDA: f64 = 0.222;

impl NormMonitor {
    pub fn new(threshold: f64, window: usize) -> Self {
        Self {
            norm_threshold: threshold,
            history: Vec::with_capacity(window),
            coherence_window: window,
            nmsi_tolerance: 1e-7,
            lucidity_depth: 0.0,
        }
    }

    pub fn covariant_weight(&self, dist: f64, delta_theta: f64) -> f64 {
        let ds = dist * (1.0 + (LAMBDA/3.0) * dist * dist).sqrt();
        ds * delta_theta.abs().exp()
    }

    pub fn nmsi_phase_shift(&self, dzo: f64, energy_gev: f64, baseline_km: f64) -> f64 {
        let dm2_eff = 2.0 * BETA_NMSI * dzo;
        OSC_CONST * dm2_eff * baseline_km / energy_gev
    }

    pub fn expected_coherence(&self, dzo_values: &[f64], energies: &[f64], baselines: &[f64]) -> f64 {
        let mut sum_cos = 0.0;
        let mut sum_sin = 0.0;
        let n = dzo_values.len() as f64;

        for i in 0..dzo_values.len() {
            let phi = self.nmsi_phase_shift(dzo_values[i], energies[i], baselines[i]);
            sum_cos += phi.cos();
            sum_sin += phi.sin();
        }

        (sum_cos * sum_cos + sum_sin * sum_sin).sqrt() / n
    }

    pub fn check_norm(&mut self, latent_state: &[f64]) -> NormDecision {
        let norm_sq: f64 = latent_state.iter().map(|x| x * x).sum();
        let norm = norm_sq.sqrt();
        let deviation = (norm - 1.0).abs();

        self.history.push(norm);
        if self.history.len() > self.coherence_window {
            self.history.remove(0);
        }

        if deviation <= self.norm_threshold {
            return NormDecision::Coherent;
        }

        if norm > 1.0 + self.norm_threshold {
            return NormDecision::DivergingHigh;
        } else if norm < 1.0 - self.norm_threshold {
            return NormDecision::DivergingLow;
        }

        NormDecision::Unstable
    }
}
