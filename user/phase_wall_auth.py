#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ARKHE-BLOCK 850.023-SEC | PHASE-WALL SIMULATOR
Simulates Layer 1 & 2 Security: Coherent Port Knocking and Entropy Filtering.
"""

import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | PHASE-WALL | %(message)s')
logger = logging.getLogger(__name__)

class PhaseWall:
    def __init__(self, gdsii_hash="0xDEADBEEF"):
        self.key = gdsii_hash
        self.entropy_threshold = 0.4

    def authenticate(self, preamble_key, l2_signal):
        logger.info(f"Layer 1: Challenging Preamble (λ₂={l2_signal:.2f})...")
        if preamble_key == self.key and l2_signal > 0.95:
            logger.info("  ✅ AUTHENTICATION SUCCESS: Coherent link established.")
            return True
        else:
            logger.error("  ❌ AUTHENTICATION FAILED: Dissonant source or invalid key.")
            return False

    def filter_entropy(self, data_packet):
        # High entropy = Malicious or Corrupted
        packet_entropy = np.std(data_packet)
        logger.info(f"Layer 2: Checking packet entropy: {packet_entropy:.3f}")

        if packet_entropy < self.entropy_threshold:
            logger.info("  ✅ PACKET CLEAN: Coherence verified.")
            return True
        else:
            logger.warning("  ⚠️ MALICIOUS DATA DETECTED: Decoupling interface!")
            return False

if __name__ == "__main__":
    pw = PhaseWall()

    # Test valid link
    pw.authenticate("0xDEADBEEF", 0.98)
    pw.filter_entropy(np.random.normal(0, 0.1, 100)) # Clean signal

    # Test attack
    logger.info("--- SIMULATING ATTACK ---")
    pw.authenticate("0xBADCODE", 0.70)
    pw.filter_entropy(np.random.uniform(0, 1, 100)) # High entropy noise
