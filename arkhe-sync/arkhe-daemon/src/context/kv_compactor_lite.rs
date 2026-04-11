pub struct LiteCompactor {
    pub mad_inertia: u32,
}

impl LiteCompactor {
    pub fn new() -> Self {
        Self { mad_inertia: 5 }
    }

    pub fn compact(&self, scores: &[f64]) -> f64 {
        if scores.is_empty() { return 0.0; }
        let mut sorted = scores.to_vec();
        sorted.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let median = sorted[sorted.len() / 2];

        let abs_dev: Vec<f64> = scores.iter().map(|&x| (x - median).abs()).collect();
        let mut sorted_dev = abs_dev;
        sorted_dev.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let mad = sorted_dev[sorted_dev.len() / 2];

        median + 1.5 * mad
    }
}
