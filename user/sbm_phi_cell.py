#!/usr/bin/env python3
"""
Phase A: φ-Unit Cell Simulation.
Coupling FDTD-EM fields with Kuramoto oscillators using EdgeOfChaosController v2.
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

    def simulate_step(self, external_field_phase):
        # 1. Calculate order parameter
        z = np.mean(np.exp(1j * self.theta))
        lambda_val = np.abs(z)

        # 2. Update K via SBM v2
        K = self.sbm.update(lambda_val)

        # 3. Kuramoto dynamics with external field coupling
        # dtheta = omega + (K/N)*sum(sin(theta_j - theta_i)) + K_ext*sin(phi_ext - theta_i)
        K_ext = 0.5
        theta_matrix = self.theta[:, None] - self.theta[None, :]
        internal_coupling = (K / self.n_nodes) * np.sum(np.sin(theta_matrix), axis=1)
        external_coupling = K_ext * np.sin(external_field_phase - self.theta)

        dtheta = self.omega + internal_coupling + external_coupling
        self.theta = (self.theta + dtheta * 0.05) % (2 * np.pi)

        self.history.append({'lambda': lambda_val, 'K': K})
        return lambda_val, K

    def run_simulation(self, steps=100):
        print(f"Starting Phase A: φ-Unit Cell Simulation ({steps} steps)...")
        for i in range(steps):
            # Simulated FDTD EM field phase rotating
            phi_ext = (i * 0.1) % (2 * np.pi)
            lam, K = self.simulate_step(phi_ext)
            if i % 20 == 0:
                print(f"Step {i}: λ₂ = {lam:.4f}, K = {K:.3f}")
        return self.history

if __name__ == "__main__":
    sim = PhiCellSimulator()
    sim.run_simulation(100)
