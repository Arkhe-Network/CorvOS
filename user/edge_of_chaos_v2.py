#!/usr/bin/env python3
"""
EdgeOfChaosController v2 – SBM-inspired adaptive coupling with anti-collapse boost.
"""

import numpy as np
from collections import deque

class EdgeOfChaosControllerV2:
    def __init__(self, initial_K=0.618, target_lambda=0.95,
                 K_min=0.3, K_max=1.5, base_rate=0.015,
                 hysteresis=0.03, history_len=50):
        self.K = initial_K
        self.target = target_lambda
        self.K_min = K_min
        self.K_max = K_max
        self.alpha = base_rate
        self.hysteresis = hysteresis

        self.lambda_history = deque(maxlen=history_len)
        self.dlambda_history = deque(maxlen=history_len)
        self.step_count = 0
        self.adaptation_gain = 1.0

    def update(self, current_lambda: float) -> float:
        self.lambda_history.append(current_lambda)

        # Calculate derivative
        if len(self.lambda_history) >= 2:
            dlambda = self.lambda_history[-1] - self.lambda_history[-2]
            self.dlambda_history.append(dlambda)
        else:
            dlambda = 0.0

        avg_dlambda = np.mean(self.dlambda_history) if self.dlambda_history else 0.0

        # Error signal
        error = current_lambda - self.target

        # Hysteresis: only update if outside range
        if abs(error) < self.hysteresis:
            delta_K = 0.0
        else:
            # SBM update rule: decrease K if too ordered, increase if too chaotic
            delta_K = -self.alpha * error
            # Damping based on velocity
            delta_K -= 0.5 * self.alpha * avg_dlambda

        # Anti-Collapse Boost
        if current_lambda < 0.8:
            delta_K += 0.12 # Emergency synchronization pulse
            self.adaptation_gain = 2.0
        else:
            self.adaptation_gain = 1.0

        self.K = np.clip(self.K + delta_K, self.K_min, self.K_max)
        self.step_count += 1
        return self.K

    def get_status(self) -> dict:
        return {
            'K': self.K,
            'last_lambda': self.lambda_history[-1] if self.lambda_history else None,
            'gain': self.adaptation_gain,
            'step': self.step_count
        }
