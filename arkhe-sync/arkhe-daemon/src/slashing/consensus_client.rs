use ethers::prelude::*;
use anyhow::Result;

pub struct ConsensusSlashingClient {
    pub contract_address: Address,
}

impl ConsensusSlashingClient {
    pub fn new(address: Address) -> Self {
        Self { contract_address: address }
    }

    pub async fn create_slashing_proposal(&self, target: Address, penalty: U256) -> Result<()> {
        println!("Slashing: Proposing penalty for {} of {}", target, penalty);
        Ok(())
    }

    pub async fn vote(&self, proposal_id: U256) -> Result<()> {
        println!("Slashing: Voting for proposal {}", proposal_id);
        Ok(())
    }
}
