#!/usr/bin/env python3
"""
Phase B: Matrix Kᵢⱼ (SBM Matrix).
Dynamical local couplings for large-scale agent synchronization.
"""

import numpy as np

class SBMMatrixSimulator:
    def __init__(self, n_agents=5, initial_K=0.618):
        self.n_agents = n_agents
        # Matrix of couplings between agents
        self.K_matrix = np.full((n_agents, n_agents), initial_K)
        self.lambdas = np.random.uniform(0.85, 0.99, n_agents)
        self.dlambdas = np.zeros(n_agents)
        self.alpha = 0.01 # Damping
        self.beta = 0.05  # Cooperation reinforcement

    def update_matrix(self):
        """
        dK_ij/dt = -alpha(K_ij - K_mean) + beta * sgn(dlambda_i/dt * dlambda_j/dt)
        """
        K_mean = np.mean(self.K_matrix)

        # Calculate sign of derivative product for all pairs
        dl_sign = np.sign(self.dlambdas)
        reinforcement = self.beta * np.outer(dl_sign, dl_sign)

        # Update rule
        damping = -self.alpha * (self.K_matrix - K_mean)
        self.K_matrix += damping + reinforcement

        # Keep K within reasonable bounds
        self.K_matrix = np.clip(self.K_matrix, 0.1, 2.0)
        return self.K_matrix

    def step(self):
        # Simulated lambda updates
        new_lambdas = self.lambdas + np.random.normal(0, 0.02, self.n_agents)
        new_lambdas = np.clip(new_lambdas, 0.0, 1.0)
        self.dlambdas = new_lambdas - self.lambdas
        self.lambdas = new_lambdas

        return self.update_matrix()

    def run_phase_b(self, steps=50):
        print(f"Starting Phase B: Matrix Kᵢⱼ Simulation ({self.n_agents} agents, {steps} steps)...")
        for i in range(steps):
            K_mat = self.step()
            if i % 10 == 0:
                print(f"Step {i}: Mean Coupling K = {np.mean(K_mat):.4f}, Diversity = {np.std(K_mat):.4f}")
        return self.K_matrix

if __name__ == "__main__":
    sim = SBMMatrixSimulator()
    sim.run_phase_b(50)
