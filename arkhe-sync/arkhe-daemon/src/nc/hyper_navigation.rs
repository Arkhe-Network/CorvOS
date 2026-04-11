use rand::Rng;

pub struct HyperNavAgent {
    q_table: Vec<Vec<f64>>,
    learning_rate: f64,
}

impl HyperNavAgent {
    pub fn new(n_states: usize, n_actions: usize) -> Self {
        Self {
            q_table: vec![vec![0.0; n_actions]; n_states],
            learning_rate: 0.1,
        }
    }

    pub fn navigate(&mut self, state: usize) -> usize {
        let mut rng = rand::thread_rng();
        if rng.gen::<f64>() < 0.1 {
            rng.gen_range(0..self.q_table[state].len())
        } else {
            0 // Simplified
        }
    }
}
