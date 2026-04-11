use ethers::signers::{LocalWallet, Signer};
use std::str::FromStr;
use anyhow::Result;

pub struct LocalWalletManager {
    pub wallet: LocalWallet,
}

impl LocalWalletManager {
    pub fn from_private_key(private_key: &str) -> Result<Self> {
        let wallet = LocalWallet::from_str(private_key)?;
        Ok(Self { wallet })
    }
}
