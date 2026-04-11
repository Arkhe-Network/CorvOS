pub struct KvCompactor {
    pub threshold: f64,
}

impl KvCompactor {
    pub fn new(threshold: f64) -> Self {
        Self { threshold }
    }

    pub fn compact(&self, cache_size: usize) -> usize {
        // Redução simulada de 50%
        (cache_size as f64 * 0.5) as usize
    }
}
