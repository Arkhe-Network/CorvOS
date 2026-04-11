use ethers::types::H256;
use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SkillMetadata {
    pub skill_id: String,
    pub price: u128,
    pub verification_key_hash: H256,
    pub active: bool,
    pub author: String,
}
