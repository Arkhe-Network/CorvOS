use std::collections::VecDeque;

pub struct TelemetryEvent {
    pub syscall_id: u32,
}

pub struct DecoherenceOracle {
    window: VecDeque<TelemetryEvent>,
    threshold: f64,
}

pub enum Warning {
    DecoherenceImminent { cycles_until_collapse: u8, recommended_action: &'static str },
}

impl DecoherenceOracle {
    pub fn new(window_size: usize) -> Self {
        Self {
            window: VecDeque::with_capacity(window_size),
            threshold: 0.85,
        }
    }

    pub fn feed(&mut self, event: TelemetryEvent) -> Option<Warning> {
        self.window.push_back(event);
        if self.window.len() < 10 {
            return None;
        }

        let entropy = self.calculate_local_entropy();
        if entropy > self.threshold {
            return Some(Warning::DecoherenceImminent {
                cycles_until_collapse: 3,
                recommended_action: "InitiateEmergencyPhase",
            });
        }
        None
    }

    fn calculate_local_entropy(&self) -> f64 {
        let values: Vec<f64> = self.window.iter().map(|e| e.syscall_id as f64).collect();
        let mean = values.iter().sum::<f64>() / values.len() as f64;
        let variance = values.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / values.len() as f64;
        variance.sqrt() / 1000.0
    }
}
