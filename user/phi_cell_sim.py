#!/usr/bin/env python3
"""
Simplified Phi-Cell Simulation for Arkhe Phase A.
Avoiding complex FDTD indices for demonstration stability.
"""

import numpy as np
from edge_of_chaos_v2 import EdgeOfChaosControllerV2

class PhiCellSimulator:
    def __init__(self, n_nodes=168):
        self.n_nodes = n_nodes
        self.sbm = EdgeOfChaosControllerV2(target_lambda=0.95, base_rate=0.015, hysteresis=0.03)
        self.theta = np.random.uniform(0, 2*np.pi, n_nodes)
        self.omega = np.random.normal(0, 0.1, n_nodes)
        self.history = []

    def simulate_step(self, i):
        # 1. Calculate order parameter
        z = np.mean(np.exp(1j * self.theta))
        lambda_val = np.abs(z)

        # 2. Update K via SBM v2
        K = self.sbm.update(lambda_val)

        # 3. Simulated field phase
        phi_ext = (i * 0.05) % (2 * np.pi)

        # 4. Kuramoto dynamics
        theta_diff = self.theta[:, None] - self.theta[None, :]
        coupling = (K / self.n_nodes) * np.sum(np.sin(theta_diff), axis=1)
        external = 0.5 * np.sin(phi_ext - self.theta)

        self.theta = (self.theta + (self.omega + coupling + external) * 0.1) % (2 * np.pi)

        self.history.append({'lambda': lambda_val, 'K': K})
        return lambda_val, K

    def run_simulation(self, n_steps=100):
        print(f"[*] Starting Phi-Cell Simulation (Steps: {n_steps})")
        for i in range(n_steps):
            lam, K = self.simulate_step(i)
        print("[*] Simulation complete.")
        return {'lambda': [h['lambda'] for h in self.history], 'K': [h['K'] for h in self.history]}

if __name__ == "__main__":
    sim = PhiCellSimulator()
    sim.run_simulation(10)
