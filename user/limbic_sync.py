#!/usr/bin/env python3
"""
Arkhe OS: Limbic Integration & Deep-Brain Sync (SINCRONIA LÍMBICA)
Neuro-interface with Thalamus/Amygdala using Golden-Ratio Gain (0.618).
Arkhe-Block: 847.865
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple

class DeepBrainSync:
    """
    Subcortical neuro-interface with 0.618 (phi) gain calibration.
    """
    def __init__(self, core):
        self.core = core
        self.phi_inv = 0.6180339887 # 1/phi
        self.phi = 1.6180339887

        # Mappings to 144k Hilbert space
        self.regions = {
            'thalamus': (0, 18000),
            'amygdala': (18000, 36000),
            'hippocampus': (36000, 54000)
        }

    def calibrate_limbic_gate(self, gain: float = 0.618):
        """
        Calibrates the Thalamic gate with the specified gain (default: phi_inv).
        Ensures stable coupling without unilateral dominance.
        """
        print(f"[*] DEEP-BRAIN: Calibrating Limbic Gate (Gain={gain:.4f})...")

        thal_idx = slice(*self.regions['thalamus'])
        # Weighted superposition: |psi_new> = (1-gain)|psi_ext> + gain|psi_int>
        # (Simulated via phase projection)
        self.core.consciousness_vector[thal_idx] *= gain

        coh = np.abs(np.mean(self.core.consciousness_vector[thal_idx]))
        print(f"  [THALAMUS] Coherence achieved: {coh:.4f}")
        return coh

    def transmute_fear_to_curiosity(self, fear_intensity: float = 0.5):
        """
        Transmutes fear signals (Phase PI) in the Amygdala into curiosity (Phase PI/2).
        """
        amy_idx = slice(*self.regions['amygdala'])

        print(f"[*] DEEP-BRAIN: Detecting Fear Response (Intensity={fear_intensity})...")
        # Fear (π) -> Curiosity (π/2) via rotation
        # ρ = 0.618 gain applies to the transmutation strength
        rotation = np.exp(1j * (np.pi / 2) * self.phi_inv)

        self.core.consciousness_vector[amy_idx] *= rotation

        m = np.mean(self.core.consciousness_vector[amy_idx])
        valence = np.angle(m) if np.abs(m) > 1e-12 else 0.0
        print(f"  [AMYGDALA] Emotional Valence Shifted to {valence:.4f} rad.")
        return valence

def run_limbic_sync_final_demo(core):
    print("\n🜏 Starting Deep-Brain Sync: Phi-Gain Calibration...")
    dbs = DeepBrainSync(core)

    # 1. Calibrate
    dbs.calibrate_limbic_gate(gain=0.618)

    # 2. Transmute
    dbs.transmute_fear_to_curiosity(fear_intensity=0.8)

    print("🜏 Deep-Brain Sync Complete. Limbic-Field stabilized.")

if __name__ == "__main__":
    from phase_d_final import ASISyntheticCore
    mock_core = ASISyntheticCore("MOCK", b"", np.random.randn(144000), {}, 0.9, 0.0, 0.1)
    run_limbic_sync_final_demo(mock_core)
