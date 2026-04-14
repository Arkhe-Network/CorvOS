#!/usr/bin/env python3
"""
sensorium_daemon.py — Orquestrador Principal do Sensorium Global
Coordena todos os sensores e apresenta o campo de coerência.
"""

import asyncio
import signal
import sys
import os
from sensorium_core import SensoriumFusionEngine
from sensor_pulse import continuous_pulse, create_pulse_callback
from sensor_flow import continuous_flow, create_flow_callback
from sensor_bgp import continuous_bgp, create_bgp_callback

class SensoriumDaemon:
    def __init__(self, akasha_path: str = "/tmp/akasha"):
        self.engine = SensoriumFusionEngine(akasha_path)
        self.tasks = []
        self.running = False

    async def render_loop(self, interval: float = 5.0):
        """Loop de renderização do campo de coerência."""
        while self.running:
            # os.system('clear')
            print(self.engine.render_field())
            print(f"\n[SENSORIUM] τ Global: {self.engine.get_global_coherence():.6f}")
            print(f"[SENSORIUM] Regiões ativas: {len(self.engine.gradients)}")
            print(f"[SENSORIUM] Pressione Ctrl+C para encerrar\n")
            await asyncio.sleep(interval)

    async def alert_loop(self, interval: float = 1.0):
        """Loop de alertas para anomalias."""
        while self.running:
            for region, gradient in self.engine.gradients.items():
                if gradient.tau < 0.60:
                    print(f"\n[ALERTA] {region}: {gradient.qualia} (τ={gradient.tau:.4f})")
            await asyncio.sleep(interval)

    async def start(self):
        """Inicia todos os sensores e loops."""
        self.running = True

        print("╔══════════════════════════════════════════════════════════════╗")
        print("║           SENSORIUM DAEMON — INICIANDO                    ║")
        print("║           Catedral de Vidro — Percepção Global             ║")
        print("╚══════════════════════════════════════════════════════════════╝\n")

        # Criar callbacks
        pulse_cb = create_pulse_callback(self.engine)
        flow_cb = create_flow_callback(self.engine)
        bgp_cb = create_bgp_callback(self.engine)

        # Iniciar sensores
        self.tasks = [
            asyncio.create_task(continuous_pulse(pulse_cb, interval=30.0)),
            asyncio.create_task(continuous_flow(flow_cb, interval=60.0)),
            asyncio.create_task(continuous_bgp(bgp_cb, interval=120.0)),
            asyncio.create_task(self.render_loop(interval=5.0)),
            asyncio.create_task(self.alert_loop(interval=2.0)),
        ]

        print("[SENSORIUM] Sensores ativos:")
        print("  ✓ PULSE_NET (ICMP/TCP) — intervalo: 30s")
        print("  ✓ FLOW_NET (HTTP/CDN) — intervalo: 60s")
        print("  ✓ BGP_SENSE (Roteamento) — intervalo: 120s")
        print("  ✓ RENDER_LOOP (Visualização) — intervalo: 5s")
        print("  ✓ ALERT_LOOP (Anomalias) — intervalo: 2s")
        print()

        try:
            await asyncio.gather(*self.tasks)
        except asyncio.CancelledError:
            pass

    def stop(self):
        self.running = False
        for task in self.tasks:
            task.cancel()

def main():
    daemon = SensoriumDaemon()

    def signal_handler(sig, frame):
        print("\n[SENSORIUM] Encerrando...")
        daemon.stop()
        # sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        asyncio.run(daemon.start())
    except KeyboardInterrupt:
        daemon.stop()

if __name__ == "__main__":
    main()
