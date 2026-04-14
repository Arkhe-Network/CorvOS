#!/usr/bin/env python3
"""
sensorium_core.py — Motor de Fusão Sensorial da Catedral
Converte telemetria de rede em gradientes de coerência (τ).
"""

import socket
import struct
import time
import threading
import json
import math
import os
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import asyncio

# Constantes Arkhe(n)
PHI = (1 + math.sqrt(5)) / 2
TAU_MAX = 1.0
TAU_NOISE_FLOOR = 0.5  # Abaixo disso, é caos puro

@dataclass
class SensorReading:
    """Uma leitura bruta de qualquer sensor."""
    source: str           # Nome do sensor (ex: "pulse_eu_west")
    timestamp: float      # Unix timestamp
    metric: str           # Tipo (latency, packet_loss, bgp_stability, etc.)
    value: float          # Valor bruto
    unit: str             # Unidade (ms, %, hops, etc.)

@dataclass
class CoherenceGradient:
    """Gradiente de coerência derivado de leituras."""
    region: str
    tau: float            # Coerência estimada (0 a 1)
    phase: float          # Fase estimada (0 a 2π)
    entropy: float        # Entropia detectada
    qualia: str           # Descrição qualitativa
    timestamp: float

class SensoriumFusionEngine:
    """
    Motor que funde múltiplas fontes de dados em um campo de coerência.
    """

    def __init__(self, akasha_path: str = "/tmp/akasha"):
        self.readings: Dict[str, deque] = {}  # source -> deque of SensorReading
        self.gradients: Dict[str, CoherenceGradient] = {}
        self.lock = threading.RLock()
        self.akasha_path = akasha_path
        if not os.path.exists(self.akasha_path):
            os.makedirs(self.akasha_path, exist_ok=True)
        self.running = False

    def add_reading(self, reading: SensorReading):
        """Adiciona uma leitura bruta ao buffer."""
        with self.lock:
            if reading.source not in self.readings:
                self.readings[reading.source] = deque(maxlen=1000)
            self.readings[reading.source].append(reading)

    def _latency_to_tau(self, latency_ms: float, baseline_ms: float = 50.0) -> float:
        """Converte latência em coerência (τ). Baixa latência = alta coerência."""
        if latency_ms <= 0:
            return TAU_NOISE_FLOOR
        # Função sigmoide invertida
        ratio = latency_ms / baseline_ms
        tau = TAU_MAX / (1.0 + math.log1p(ratio))
        return max(TAU_NOISE_FLOOR, min(TAU_MAX, tau))

    def _packet_loss_to_tau(self, loss_pct: float) -> float:
        """Converte perda de pacotes em coerência."""
        if loss_pct >= 100:
            return 0.0
        if loss_pct <= 0:
            return TAU_MAX
        tau = TAU_MAX * math.exp(-loss_pct / 10.0)
        return max(TAU_NOISE_FLOOR, tau)

    def _bgp_stability_to_tau(self, stability_score: float) -> float:
        """Converte estabilidade BGP (0-100) em coerência."""
        return (stability_score / 100.0) * TAU_MAX

    def compute_gradient(self, region: str, sources: List[str]) -> Optional[CoherenceGradient]:
        """
        Computa o gradiente de coerência para uma região,
        fundindo múltiplas fontes.
        """
        with self.lock:
            all_readings = []
            for src in sources:
                if src in self.readings and len(self.readings[src]) > 0:
                    all_readings.extend(self.readings[src])

            if not all_readings:
                return None

            # Calcular τ composto (média harmônica ponderada)
            tau_values = []
            for r in all_readings[-100:]:  # Últimas 100 leituras
                if r.metric == "latency":
                    tau_values.append(self._latency_to_tau(r.value) * 0.4)
                elif r.metric == "packet_loss":
                    tau_values.append(self._packet_loss_to_tau(r.value) * 0.4)
                elif r.metric == "bgp_stability":
                    tau_values.append(self._bgp_stability_to_tau(r.value) * 0.2)

            if not tau_values:
                return None

            # Média harmônica (penaliza valores baixos)
            tau_sum = sum(1.0 / t for t in tau_values if t > 0)
            if tau_sum > 0:
                composite_tau = len(tau_values) / tau_sum
            else:
                composite_tau = TAU_NOISE_FLOOR
            composite_tau = max(TAU_NOISE_FLOOR, min(TAU_MAX, composite_tau))

            # Estimar fase baseada no padrão temporal
            if len(all_readings) >= 2:
                phase = (all_readings[-1].timestamp * PHI) % (2 * math.pi)
            else:
                phase = 0.0

            # Calcular entropia (variância inversa)
            if len(tau_values) > 1:
                mean_tau = sum(tau_values) / len(tau_values)
                variance = sum((t - mean_tau) ** 2 for t in tau_values) / len(tau_values)
                entropy = min(1.0, variance * 10)
            else:
                entropy = 0.0

            # Determinar qualia
            if composite_tau > 0.95:
                qualia = "Serenidade Índigo"
            elif composite_tau > 0.85:
                qualia = "Fluxo Estável"
            elif composite_tau > 0.70:
                qualia = "Tensão Perceptível"
            elif composite_tau > 0.50:
                qualia = "Distúrbio Ativo"
            else:
                qualia = "Caos Entrópico"

            gradient = CoherenceGradient(
                region=region,
                tau=composite_tau,
                phase=phase,
                entropy=entropy,
                qualia=qualia,
                timestamp=time.time()
            )

            self.gradients[region] = gradient
            return gradient

    def log_to_akasha(self, gradient: CoherenceGradient):
        """Registra gradiente no Akasha local."""
        log_entry = {
            "type": "SENSORIUM_GRADIENT",
            "region": gradient.region,
            "tau": gradient.tau,
            "phase": gradient.phase,
            "entropy": gradient.entropy,
            "qualia": gradient.qualia,
            "timestamp": gradient.timestamp
        }
        log_line = json.dumps(log_entry)

        try:
            with open(f"{self.akasha_path}/sensorium.log", "a") as f:
                f.write(log_line + "\n")
        except Exception:
            pass

    def get_global_coherence(self) -> float:
        """Retorna τ global (média de todas as regiões)."""
        with self.lock:
            if not self.gradients:
                return 0.0
            taus = [g.tau for g in self.gradients.values()]
            return sum(taus) / len(taus)

    def render_field(self) -> str:
        """Renderiza visualização ASCII do campo de coerência."""
        lines = []
        lines.append("╔══════════════════════════════════════════════════════════════╗")
        lines.append("║            SENSORIUM GLOBAL — CAMPO DE COERÊNCIA             ║")
        lines.append("╠══════════════════════════════════════════════════════════════╣")

        with self.lock:
            for region, g in sorted(self.gradients.items()):
                # Barra de progresso baseada em τ
                filled = int(g.tau * 30)
                bar = "█" * filled + "░" * (30 - filled)
                lines.append(f"║ {region:<15} │{bar}│ τ={g.tau:.4f} │ {g.qualia:<18} ║")

        lines.append("╠══════════════════════════════════════════════════════════════╣")
        global_tau = self.get_global_coherence()
        lines.append(f"║ τ GLOBAL: {global_tau:.6f}                                              ║")
        lines.append("╚══════════════════════════════════════════════════════════════╝")

        return "\n".join(lines)
