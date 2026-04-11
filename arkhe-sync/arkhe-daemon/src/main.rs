mod tui;
mod oracle;
mod distill;
mod resonance;
mod collapse;
mod asi_gate;
mod kv_compactor;
mod evolution;
mod network;
mod engine;
mod context;
mod orchestration;
mod governance;
mod offline;
mod marketplace;
mod slashing;

use crate::tui::{DreamSync, QuantumState};
use crate::oracle::{DecoherenceOracle, TelemetryEvent};
use crate::distill::SkillDistillery;
use crate::resonance::ResonanceField;
use crate::collapse::{ControlledCollapse, SafeState};
use crate::asi_gate::{AsimovGate, GateDecision};
use crate::kv_compactor::KvCompactor;
use crate::evolution::EvolutionEngine;
use crate::evolution::auto_repair::AutoRepairOracle;
use crate::network::libp2p_discovery::{Libp2pDiscovery, ArkheNodeAnnounce};
use crate::orchestration::liquid::LiquidOrchestrator;
use crate::marketplace::MarketplaceClient;
use crate::governance::GovernanceClient;
use crate::slashing::consensus_client::ConsensusSlashingClient;
use crate::engine::rem_modulator;
use ethers::types::Address;

#[tokio::main]
async fn main() {
    println!("🜏 Arkhe-Sync Daemon v2.0.0-omnichain (Época 1443 Final) starting...");

    let mut tui = DreamSync::new();
    let mut oracle = DecoherenceOracle::new(100);
    let mut distillery = SkillDistillery::new();
    let resonance = ResonanceField::new();
    let mut gate = AsimovGate::new();
    let evolution = EvolutionEngine::new();
    let discovery = Libp2pDiscovery::new();
    let liquid = LiquidOrchestrator::new("node_local".to_string());
    let marketplace = MarketplaceClient::new("0x0000000000000000000000000000000000000000000000000000000000000001").unwrap();
    let governance = GovernanceClient::new(Address::zero());
    let slashing = ConsensusSlashingClient::new(Address::zero());
    let auto_repair = AutoRepairOracle::new(0.20);

    // Arkhe-Lab endpoints (simulated via match logic in real scenario)
    println!("Arkhe-Lab: /predict and /experiment endpoints ready.");

    let mut epoch: u64 = 0;

    loop {
        let event = TelemetryEvent { syscall_id: 1 };
        let telemetry = vec![120.0, 0.99];

        let epsilon = rem_modulator::compute_epsilon(0.95, epoch);
        let decision = gate.evaluate(0.9997, &telemetry);

        evolution.process_telemetry(&telemetry, epoch).await;

        if epoch % 10 == 0 {
            liquid.register_task(format!("task_{}", epoch)).await;
            marketplace.register_skill(&format!("skill_{}", epoch), 10.into()).await.unwrap();
            governance.create_proposal(&format!("Proposal {}", epoch)).await.unwrap();
            auto_repair.monitor_and_propose_upgrade("short_circuit_detector", 0.25).await.unwrap();
        }

        let announce = ArkheNodeAnnounce {
            node_id: vec![0],
            udp_endpoint: "localhost:1337".to_string(),
            coherence: 0.9997,
            timestamp: epoch,
            vram_gb: 24,
            wormhole_ids: vec![1, 2, 3],
        };
        discovery.announce(announce).await;

        tui.update(QuantumState { fidelity: 0.9997 });
        tui.render();

        if epoch % 20 == 0 {
            println!("Epoch: {} | ε: {:.4} | Substrate: COHERENT", epoch, epsilon);
        }

        epoch += 1;
        if epoch >= 1000 { break; }
        tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
    }

    println!("🜏 Evolution Cycle Completed. System Stabilized at Época 1443.");
}
