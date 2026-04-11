pub struct Wormhole {
    pub from: usize,
    pub to: usize,
    pub strength: f64,
}

pub struct ResonanceField {
    local_coherence: f64,
    wormholes: Vec<Wormhole>,
}

impl ResonanceField {
    pub fn new() -> Self {
        Self {
            local_coherence: 1.0,
            wormholes: vec![
                Wormhole { from: 127, to: 1003, strength: 0.99 },
                Wormhole { from: 89, to: 2047, strength: 0.98 },
            ]
        }
    }

    pub async fn broadcast_state(&self, _root: &[u8; 32], _sig: &[u8; 32]) {
        println!("Broadcasting Resonance State across Hypergraph...");
    }
}
