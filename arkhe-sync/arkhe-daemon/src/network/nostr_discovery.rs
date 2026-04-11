use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Clone)]
pub struct NodeCapabilities {
    pub udp_endpoint: String,
    pub coherence: f64,
}

pub struct NostrDiscovery {
    peers: Arc<RwLock<HashMap<String, NodeCapabilities>>>,
}

impl NostrDiscovery {
    pub fn new() -> Self {
        Self {
            peers: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    pub async fn announce(&self, _endpoint: String) {
        println!("Announcing node via Nostr...");
    }

    pub async fn get_peers(&self) -> HashMap<String, NodeCapabilities> {
        self.peers.read().await.clone()
    }
}
