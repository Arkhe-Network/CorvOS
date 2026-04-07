#!/usr/bin/env python3
"""
Rio-Collective: Agent-Based Modeling Environment for Urban Coherence.
Simulates the Rio de Janeiro urban grid where multiple agents interact.
"""

import numpy as np
from typing import List, Dict, Any

class UrbanEnvironment:
    def __init__(self, num_agents: int = 3):
        self.num_agents = num_agents
        self.t = 0
        self.global_lambda = 0.95
        self.agent_positions = np.random.rand(num_agents, 2) # X, Y coordinates
        self.history = []

    def reset(self) -> Dict[int, Dict[str, Any]]:
        self.t = 0
        self.global_lambda = 0.95
        return self._generate_observations()

    def _generate_observations(self) -> Dict[int, Dict[str, Any]]:
        obs = {}
        for i in range(self.num_agents):
            obs[i] = {
                't': self.t,
                'lambda_global': self.global_lambda,
                'summary': f"Urban state at tick {self.t}",
                'neighbors': self._get_neighbors(i)
            }
        return obs

    def _get_neighbors(self, agent_idx: int) -> List[int]:
        # Simple distance-based proximity
        pos = self.agent_positions[agent_idx]
        distances = np.linalg.norm(self.agent_positions - pos, axis=1)
        return [i for i, d in enumerate(distances) if d < 0.5 and i != agent_idx]

    def step(self, actions: Dict[int, Dict[str, Any]]) -> tuple:
        """
        Processes agent actions and updates global coherence.
        """
        self.t += 1

        # Calculate coherence change based on cooperation
        cooperation_count = sum(1 for a in actions.values() if a['action'] == "COOPERATE")

        # Emergent behavior logic: λ₂ increases if more agents cooperate
        reward_factor = (cooperation_count / self.num_agents) - 0.5
        self.global_lambda = np.clip(self.global_lambda + (reward_factor * 0.05), 0.0, 1.0)

        new_obs = self._generate_observations()
        rewards = {i: self.global_lambda for i in range(self.num_agents)}
        done = self.t >= 50 or self.global_lambda > 0.999

        self.history.append({
            't': self.t,
            'cooperation': cooperation_count,
            'lambda': self.global_lambda
        })

        return new_obs, rewards, done, {}

    def get_final_report(self) -> Dict[str, Any]:
        return {
            'total_ticks': self.t,
            'final_lambda': self.global_lambda,
            'coherence_trajectory': [h['lambda'] for h in self.history]
        }
