pub fn compute_rem_factor(epoch: u64) -> f64 {
    let t_secs = epoch * 5;
    let phase = 2.0 * std::f64::consts::PI * (t_secs as f64 / 5400.0);
    1.0 + 0.05 * phase.sin()
}

pub fn compute_epsilon(base_epsilon: f64, epoch: u64) -> f64 {
    let rem = compute_rem_factor(epoch);
    (base_epsilon * rem).clamp(0.8, 1.1)
}
