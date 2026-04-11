use anyhow::Result;
use ethers::prelude::*;
use std::sync::Arc;

pub struct MarketplaceClient {
    pub wallet_manager: super::wallet::LocalWalletManager,
}

impl MarketplaceClient {
    pub fn new(private_key: &str) -> Result<Self> {
        let wallet_manager = super::wallet::LocalWalletManager::from_private_key(private_key)?;
        Ok(Self { wallet_manager })
    }

    pub async fn register_skill(&self, skill_id: &str, price: U256) -> Result<()> {
        println!("Marketplace: Registering skill {} with price {}", skill_id, price);
        Ok(())
    }
}
