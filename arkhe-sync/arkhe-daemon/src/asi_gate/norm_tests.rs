#[cfg(test)]
mod tests {
    use crate::asi_gate::norm_monitor::{NormMonitor, NormDecision};

    #[test]
    fn test_norm_unitary() {
        let mut monitor = NormMonitor::new(0.05, 10);
        let state = vec![0.7071, 0.7071];
        let result = monitor.check_norm(&state);
        assert!(matches!(result, NormDecision::Coherent));
    }

    #[test]
    fn test_nmsi_logic() {
        let monitor = NormMonitor::new(0.05, 10);
        let shift = monitor.nmsi_phase_shift(0.5, 1000.0, 10000.0);
        assert!(shift > 0.0);
    }
}
