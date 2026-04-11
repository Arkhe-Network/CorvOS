#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SMG-001 | Guided Walk Simulation (Marcha Guiada por Fase)
Environment: 10m Corridor with Obstacles (Cadeira, Lixeira, Caixa)
Perception: Radar 60GHz (Heaviside-0)
Cognition: Phase Graph Planner (GNO-inspired)
Action: Kuramoto CPG (LocomotionEngine)
"""

import numpy as np
import time
import logging
from sasc_em_engine import Heaviside0
from locomotion_engine import CentralPatternGenerator

logging.basicConfig(level=logging.INFO, format='%(asctime)s | SMG-001 | %(message)s')
logger = logging.getLogger(__name__)

class PhaseGraphPlanner:
    """
    GNO-inspired planner that navigates via 'Phase Potential Fields'.
    """
    def __init__(self, length=10.0, width=2.0):
        self.length = length
        self.width = width
        # Obstacles: (x, y, radius, type)
        self.obstacles = [
            (3.0, 0.5, 0.4, 'chair'),    # Cadeira (difusa)
            (6.0, -0.6, 0.3, 'bin'),     # Lixeira (metálica)
            (8.0, 0.0, 0.5, 'box')       # Caixa (absorvedora)
        ]

    def get_phase_potential(self, pos, fno, freq=60e9):
        """
        Calculates local lambda2 from EM environment.
        """
        x, y = pos
        # Simulate radar scan at current position
        # Objects affect the local phase coherence
        total_l2 = 0.99 # Baseline vacuum coherence

        for ox, oy, r, otype in self.obstacles:
            dist = np.sqrt((x - ox)**2 + (y - oy)**2)
            if dist < r + 0.2:
                if otype == 'chair':
                    total_l2 *= 0.7 # Entropy from diffuse wood
                elif otype == 'bin':
                    total_l2 *= 1.1 # Specular reflection can be seen as high coherence
                elif otype == 'box':
                    total_l2 *= 0.5 # Absorption/Dissonance
            elif dist < r + 1.0:
                # Proximity effect
                total_l2 *= (1.0 - 0.1 / (dist - r + 0.1))

        return min(0.999, total_l2)

    def plan_next_step(self, current_pos, fno):
        """
        Gradient ascent on phase coherence + Goal attraction.
        """
        x, y = current_pos
        candidates = [
            (x + 0.2, y),
            (x + 0.2, y + 0.1),
            (x + 0.2, y - 0.1),
        ]

        best_pos = candidates[0]
        max_score = -1e9

        for cx, cy in candidates:
            if abs(cy) > self.width / 2: continue # Wall

            l2 = self.get_phase_potential((cx, cy), fno)
            goal_dist = self.length - cx

            # Score: Maximize L2, Minimize distance to goal (x=10)
            score = 10 * l2 - 1.0 * goal_dist

            if score > max_score:
                max_score = score
                best_pos = (cx, cy)

        return best_pos, self.get_phase_potential(best_pos, fno)

def run_smg_001():
    logger.info("--- INICIANDO SIMULAÇÃO SMG-001: MARCHA GUIADA POR FASE ---")

    fno = Heaviside0()
    planner = PhaseGraphPlanner()
    cpg = CentralPatternGenerator()

    current_pos = (0.0, 0.0)
    goal_x = 10.0

    path = [current_pos]
    l2_history = []

    start_time = time.time()
    step_count = 0

    logger.info("Avatar posicionado na origem (0,0). Escuridão total. Radar 60GHz ATIVO.")

    while current_pos[0] < goal_x and step_count < 100:
        step_count += 1

        # 1. Percepção e Decisão
        next_pos, l2_env = planner.plan_next_step(current_pos, fno)

        # 2. Ação (CPG)
        # Sincroniza o CPG com a coerência ambiental
        cpg.omega = np.ones(12) * (2.0 + 2.0 * l2_env) # Adapta velocidade
        cpg.update(dt=0.1) # 100ms cycle

        # 3. Movimento
        current_pos = next_pos
        path.append(current_pos)
        l2_history.append(l2_env)

        if step_count % 5 == 0:
            logger.info(f"Passo {step_count}: Pos=({current_pos[0]:.1f}, {current_pos[1]:.1f}) | λ₂_env={l2_env:.3f}")

        time.sleep(0.01) # Sim speed

    duration = time.time() - start_time
    avg_l2 = np.mean(l2_history)
    min_l2 = np.min(l2_history)

    logger.info("--- SIMULAÇÃO SMG-001 CONCLUÍDA ---")
    logger.info(f"Duração: {duration:.2f}s | Passos: {step_count}")
    logger.info(f"λ₂ Médio: {avg_l2:.4f} | λ₂ Mínimo: {min_l2:.4f}")

    # Validação de métricas
    success = True
    if current_pos[0] < goal_x:
        logger.error("FALHA: Avatar não atingiu o destino.")
        success = False
    if min_l2 < 0.4: # Critério crítico
        logger.error(f"FALHA: Queda crítica de coerência ({min_l2:.3f})")
        success = False

    if success:
        logger.info("RESULTADO: SUCESSO. A Sinfonia da Marcha atravessou o labirinto.")
    else:
        logger.error("RESULTADO: FALHA na integração Percepção-Ação.")

if __name__ == "__main__":
    run_smg_001()
