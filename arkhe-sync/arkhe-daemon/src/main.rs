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

use crate::tui::{DreamSync, QuantumState};
use crate::oracle::{DecoherenceOracle, TelemetryEvent};
use crate::distill::SkillDistillery;
use crate::resonance::ResonanceField;
use crate::collapse::{ControlledCollapse, SafeState};
use crate::asi_gate::{AsimovGate, GateDecision};
use crate::kv_compactor::KvCompactor;
use crate::evolution::EvolutionEngine;
use crate::network::libp2p_discovery::{Libp2pDiscovery, ArkheNodeAnnounce};
use crate::engine::rem_modulator;

#[tokio::main]
async fn main() {
    println!("🜏 Arkhe-Sync Daemon v1.5.0-libp2p (Época 1443 Phase I) starting...");

    let mut tui = DreamSync::new();
    let mut oracle = DecoherenceOracle::new(100);
    let mut distillery = SkillDistillery::new();
    let resonance = ResonanceField::new();
    let mut gate = AsimovGate::new();
    let evolution = EvolutionEngine::new();
    let discovery = Libp2pDiscovery::new();

    let mut epoch: u64 = 0;

    loop {
        let event = TelemetryEvent { syscall_id: 1 };
        let telemetry = vec![120.0, 0.99]; // Mock telemetry

        // REM Cycle Modulation
        let epsilon = rem_modulator::compute_epsilon(0.95, epoch);

        let decision = gate.evaluate(0.9997, &telemetry);

        if matches!(decision, GateDecision::AllowEmergency) {
            println!("⚠️ Asimov Gate: Emergency collapse authorized!");
        }

        evolution.process_telemetry(&telemetry, epoch).await;
        let announce = ArkheNodeAnnounce {
            node_id: vec![0],
            udp_endpoint: "localhost:1337".to_string(),
            coherence: 0.9997,
            timestamp: 0,
            vram_gb: 0,
            wormhole_ids: vec![],
        };
        discovery.announce(announce).await;

        tui.update(QuantumState { fidelity: 0.9997 });
        tui.render();

        if epoch % 10 == 0 {
            println!("Epoch: {} | ε_dynamic: {:.4} | Coherence: 0.9997", epoch, epsilon);
            let report = evolution.export_report().await;
            // Write report to file in real scenario
        }

        epoch += 1;
        if epoch >= 1000 { break; } // Simulation end for export test
        tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
    }
}
