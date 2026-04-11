use anyhow::Result;
use ethers::prelude::*;

pub struct CrossChainMarketplace {
    pub local_client: super::client::MarketplaceClient,
}

impl CrossChainMarketplace {
    pub fn new(local_client: super::client::MarketplaceClient) -> Self {
        Self { local_client }
    }

    pub async fn purchase_remote_skill(&self, dst_chain_id: u16, skill_id: &str) -> Result<()> {
        println!("CrossChain: Purchasing skill {} from chain {}", skill_id, dst_chain_id);
        Ok(())
    }
}
