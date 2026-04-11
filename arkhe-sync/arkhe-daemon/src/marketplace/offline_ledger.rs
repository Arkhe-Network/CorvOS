use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use libp2p::PeerId;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub enum TxType {
    RegisterSkill,
    PurchaseSkill,
    ReportOutcome,
    Vote,
}

#[derive(Serialize, Deserialize, Clone, Debug)]
pub struct OfflineTx {
    pub tx_type: TxType,
    pub payload: Vec<u8>,
    pub signature: Vec<u8>,
    pub timestamp: u64,
    pub node_id: String,
}

pub struct OfflineLedger {
    pub pending_txs: HashMap<String, OfflineTx>,
}

impl OfflineLedger {
    pub fn new() -> Self {
        Self {
            pending_txs: HashMap::new(),
        }
    }

    pub fn add_tx(&mut self, hash: String, tx: OfflineTx) {
        self.pending_txs.insert(hash, tx);
    }
}
