use libp2p::{
    gossipsub,
    swarm::NetworkBehaviour,
    PeerId,
};
use prost::Message;
use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use tokio::sync::RwLock;

#[derive(Clone, PartialEq, Message, Serialize, Deserialize)]
pub struct ArkheNodeAnnounce {
    #[prost(bytes, tag = "1")]
    pub node_id: Vec<u8>,
    #[prost(string, tag = "2")]
    pub udp_endpoint: String,
    #[prost(double, tag = "3")]
    pub coherence: f64,
    #[prost(uint64, tag = "4")]
    pub timestamp: u64,
    #[prost(uint32, tag = "5")]
    pub vram_gb: u32,
    #[prost(uint32, repeated, tag = "6")]
    pub wormhole_ids: Vec<u32>,
}

pub struct Libp2pDiscovery {
    pub active_peers: RwLock<HashMap<PeerId, ArkheNodeAnnounce>>,
}

impl Libp2pDiscovery {
    pub fn new() -> Self {
        Self {
            active_peers: RwLock::new(HashMap::new()),
        }
    }

    pub async fn announce(&self, _announce: ArkheNodeAnnounce) {
        println!("Announcing capabilities via libp2p...");
    }

    pub async fn run(&self) {
        println!("Libp2p discovery swarm running...");
    }
}
