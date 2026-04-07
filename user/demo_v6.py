#!/usr/bin/env python3
"""
Arkhe OS v6.0 Demonstration: The Universal Organism.
Integrates PGC v4.1, Shachi Agents, SBM Control, QEP Compression, and Arkhe-Talk.
"""

from arkhe_pgc import ArkhePGC, simulate_realistic_gwas, PathwayCoherenceAnalyzer, SingleCellEqtlMapper, CrossDisorderAnalyzer
from arkhe_shachi import ArkheAgent
from rio_collective import UrbanEnvironment
from edge_of_chaos_controller import EdgeOfChaosController
from arkhe_compress import ArkheQEP
from arkhe_talk import ArkheTalk
import numpy as np
import os

def run_v6_demo():
    print("🌌 Arkhe OS v6.0: Universal Organism Simulation")
    print("="*60)

    # 1. Genetic Architecture (PGC v4.1)
    print("\n[1/5] Mapping Functional Phase Architecture...")
    pgc = ArkhePGC()
    scz_df = simulate_realistic_gwas(n_snps=2000, seed=42)
    bip_df = simulate_realistic_gwas(n_snps=2000, seed=123)

    scz_df = pgc.calculate_metrics(scz_df)
    scz_pruned = pgc.ld_clumping(scz_df)

    mapper = SingleCellEqtlMapper()
    snp_to_gene = mapper.simulate_mapping(scz_pruned['SNP'].tolist())

    pathway_db = {'Synaptic_Sync': {f'SC_NEURON_GENE_{i}' for i in range(100)}}
    pca = PathwayCoherenceAnalyzer(pathway_db)
    path_report = pca.calculate_pathway_coherence(scz_pruned, snp_to_gene, min_snps=1)

    base_lambda = pgc.compute_coherence(scz_pruned)
    print(f"Base Genetic Coherence: {base_lambda:.4f}")
    print(f"Top Pathway Coherence: {path_report['lambda2_internal'].iloc[0]:.4f}")

    # 2. Agent Compression (QEP)
    print("\n[2/5] Optimizing Agent Weights (Phase-Aware QEP)...")
    qep = ArkheQEP(bitwidth=4)
    # Simulate a small weight matrix
    weights = np.random.rand(5, 5)
    phases = np.random.rand(5, 5) * 2 * np.pi
    comp_w, corr_p = qep.compress_agent_matrix(weights, phases)
    print(f"Matrix Compressed. Average Phase Shift: {np.mean(corr_p - phases):.4f} rad")

    # 3. Collective ABM with SBM Control
    print("\n[3/5] Running Collective Simulation (Edge of Chaos)...")
    talk = ArkheTalk()
    sbm = EdgeOfChaosController(initial_K=0.618, target_lambda=0.95)
    env = UrbanEnvironment(num_agents=3)

    # Initialize Shachi Agents
    agents = [ArkheAgent(f"Agent-{i}", {'genetic_bias': base_lambda}) for i in range(3)]

    obs = env.reset()
    for tick in range(10):
        # SBM coupling update
        K = sbm.update(env.global_lambda)

        actions = {i: agents[i].step(obs[i]) for i in range(3)}
        obs, rewards, done, _ = env.step(actions)

        if tick % 5 == 0:
            print(f"Tick {tick}: λ₂ = {env.global_lambda:.4f}, K = {K:.3f}")
            talk.publish_coherence_report(f"System-Daemon", env.global_lambda, f"Stability high. K={K:.3f}")

    # 4. Results
    print("\n[4/5] Simulation Complete.")
    print(f"Final Global Coherence: {env.global_lambda:.4f}")

    # 5. Social Feed
    print("\n[5/5] Arkhe-Talk Global Feed:")
    for post in talk.get_feed():
        print(post)

    print("\n" + "="*60)
    print("Arkhe OS v6.0 Deployment Successful.")

if __name__ == "__main__":
    run_v6_demo()
