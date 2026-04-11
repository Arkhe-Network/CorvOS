pub struct TelemetryProof {
    pub merkle_root: [u8; 32],
    pub proof_data: Vec<u8>,
}

pub struct StarkProver;

impl StarkProver {
    pub fn prove(&self, _data: &[u8]) -> TelemetryProof {
        TelemetryProof {
            merkle_root: [0u8; 32],
            proof_data: vec![],
        }
    }
}
