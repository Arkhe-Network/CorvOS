#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARKHE-BLOCK 850.023-BUB | CAVITY RESONANCE SIMULATOR
Exorcising the 'Gaiola de Faraday'.
"""

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | CAVITY-SIM | %(message)s')
logger = logging.getLogger(__name__)

class CavityResonanceSim:
    def __init__(self, L=0.25, W=0.18, H=0.08):
        self.L = L # 250mm
        self.W = W # 180mm
        self.H = H # 80mm
        self.c = 299792458

    def find_eigenmodes(self, max_freq_ghz=70):
        logger.info(f"Simulating Eigenmodes for {self.L*1000}x{self.W*1000}x{self.H*1000}mm cavity...")
        modes = []
        for m in range(5):
            for n in range(5):
                for p in range(5):
                    if m+n+p == 0: continue
                    f = (self.c / 2) * np.sqrt((m/self.L)**2 + (n/self.W)**2 + (p/self.H)**2)
                    if f/1e9 < max_freq_ghz:
                        modes.append((m, n, p, f/1e9))

        # Sort by frequency
        modes.sort(key=lambda x: x[3])

        # Check critical bands
        cpg_band = 0.9 # GHz
        radar_band = (57, 64) # GHz

        for m, n, p, f in modes:
            status = "  "
            if abs(f - cpg_band) < 0.05:
                status = "⚠️ CRITICAL (CPG Band): "
            elif radar_band[0] <= f <= radar_band[1]:
                status = "⚠️ CRITICAL (Radar Band): "

            if "CRITICAL" in status:
                logger.warning(f"{status} Mode({m},{n},{p}) at {f:.2f} GHz")
            elif f < 10:
                logger.info(f"  Mode({m},{n},{p}) at {f:.2f} GHz")

        logger.info(f"Exorcism complete: {len(modes)} modes identified.")
        logger.info("Recommendation: Apply ECCOSORB foam to dampen Q factor of modes in 57-64GHz band.")

if __name__ == "__main__":
    sim = CavityResonanceSim()
    sim.find_eigenmodes()
