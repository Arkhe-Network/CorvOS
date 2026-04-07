#!/usr/bin/env python3
"""
Arkhe OS v5.0 Demonstration: Collective Intelligence Framework.
Integrates Arkhe-PGC (Genetics), Arkhe-Shachi (Agents), and Rio-Collective (ABM).
"""

from arkhe_pgc import ArkhePGC, simulate_realistic_gwas
from arkhe_shachi import ArkheAgent
from rio_collective import UrbanEnvironment
import numpy as np

def run_collective_demo():
    print("🌌 Arkhe OS v5.0: Collective Intelligence Simulation")
    print("="*60)

    # 1. Genetic Foundation (Arkhe-PGC)
    print("\n[1/4] Establishing Genetic Foundation...")
    pgc = ArkhePGC()
    gwas_df = simulate_realistic_gwas(n_snps=2000, seed=42)
    gwas_df = pgc.calculate_metrics(gwas_df)
    pruned_df = pgc.ld_clumping(gwas_df)

    # Extract functional coherence as a bias for agents
    global_coherence_bias = pgc.compute_coherence(pruned_df)
    print(f"Base Genetic Coherence (λ₂): {global_coherence_bias:.4f}")

    # 2. Agent Initialization (Arkhe-Shachi)
    print("\n[2/4] Initializing Shachi-based Urban Agents...")
    num_agents = 5
    agents = []
    # Each agent represents a different urban sector with slightly different biases
    sector_names = ["Traffic", "Energy", "Social", "Health", "Gov"]

    for i in range(num_agents):
        config = {
            'sector': sector_names[i],
            'genetic_bias': global_coherence_bias * (0.8 + 0.4 * np.random.rand()),
            'initial_lambda': 0.95
        }
        agents.append(ArkheAgent(agent_id=f"Rio-{sector_names[i]}", config=config))
        print(f"Created Agent {agents[-i-1].agent_id} with bias {config['genetic_bias']:.3f}")

    # 3. Collective Simulation (Rio-Collective)
    print("\n[3/4] Running Urban Collective Simulation...")
    env = UrbanEnvironment(num_agents=num_agents)
    observations = env.reset()

    done = False
    while not done:
        actions = {}
        for i in range(num_agents):
            actions[i] = agents[i].step(observations[i])

        observations, rewards, done, _ = env.step(actions)

        # Update agents with new global state
        for i in range(num_agents):
            agents[i].update_coherence(rewards[i])

        if env.t % 10 == 0:
            print(f"Tick {env.t}: Global λ₂ = {env.global_lambda:.4f}")

    # 4. Final Report
    print("\n[4/4] Simulation Complete. Generating Emergent Coherence Report...")
    report = env.get_final_report()
    print("-" * 30)
    print(f"Final Global Coherence: {report['final_lambda']:.4f}")
    print(f"Total Convergence Time: {report['total_ticks']} ticks")

    if report['final_lambda'] > 0.99:
        print("\n✅ Result: SOVEREIGN OMEGA STATE ACHIEVED.")
        print("The urban grid has reached collective phase-lock.")
    else:
        print("\n⚠️ Result: Sub-optimal coherence. Further genetic refinement required.")

    print("\n" + "="*60)
    print("Conclusion: Arkhe-Shachi agents successfully mapped genetic phase")
    print("biases into collective urban synchronization.")

if __name__ == "__main__":
    run_collective_demo()
