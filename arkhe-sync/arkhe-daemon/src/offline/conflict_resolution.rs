use std::collections::HashMap;
use std::cmp::Ordering;
use serde::{Serialize, Deserialize};
use ethers::types::{Address, H256};

#[derive(Clone, Debug, Serialize, Deserialize, Eq, PartialEq)]
pub enum TxType {
    RegisterSkill { skill_id: String, price: u128, vk_hash: H256 },
    PurchaseSkill { skill_id: String, buyer: Address, price: u128 },
    ReportOutcome { skill_id: String, success: bool, reporter: Address },
    Vote { proposal_id: u64, support: bool },
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct OfflineTransaction {
    pub tx_type: TxType,
    pub node_id: String,
    pub timestamp: u64,
    pub hash: Vec<u8>,
}

pub trait ReputationOracleClient {
    fn get_reputation(&self, node_id: &str) -> Option<H256>;
}

pub fn resolve_conflicts(
    local_txs: Vec<OfflineTransaction>,
    remote_txs: Vec<OfflineTransaction>,
) -> Vec<OfflineTransaction> {
    let mut all_txs: Vec<OfflineTransaction> = local_txs.into_iter().chain(remote_txs.into_iter()).collect();
    // Simplified resolution logic for simulation: sort by timestamp
    all_txs.sort_by(|a, b| a.timestamp.cmp(&b.timestamp));
    all_txs
}
