#!/usr/bin/env python3
"""
sensor_pulse.py — Sensor de Pulso de Rede (ICMP/TCP)
Mede latência e perda de pacotes para alvos globais.
"""

import asyncio
import socket
import time
import struct
import sys
from dataclasses import dataclass
from typing import List, Tuple
import subprocess

# Alvos globais por região
GLOBAL_TARGETS = {
    "na_east": [
        ("8.8.8.8", "Google DNS"),
        ("1.1.1.1", "Cloudflare DNS"),
    ],
    "na_west": [
        ("8.8.4.4", "Google DNS Secondary"),
        ("9.9.9.9", "Quad9 DNS"),
    ],
    "eu_west": [
        ("208.67.222.222", "OpenDNS"),
        ("185.228.168.9", "CleanBrowsing"),
    ],
    "ap_south": [
        ("1.0.0.1", "Cloudflare APAC"),
    ],
    "sa_east": [
        ("200.155.254.3", "NIC Brazil"),
        ("201.49.148.2", "Vivo DNS"),
    ],
}

@dataclass
class PingResult:
    target: str
    latency_ms: float
    packet_loss_pct: float
    reachable: bool

async def async_ping(host: str, count: int = 3, timeout: float = 2.0) -> PingResult:
    """Executa ping assíncrono via subprocess."""
    try:
        cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout * count + 1)
        output = stdout.decode()

        # Parse resultado
        latency = None
        loss = 100.0

        for line in output.split("\n"):
            if "rtt min/avg/max" in line:
                parts = line.split("=")[1].split("/")
                latency = float(parts[1])  # avg
            if "packet loss" in line:
                try:
                    loss_str = line.split("%")[0].split()[-1]
                    loss = float(loss_str)
                except:
                    pass

        if latency is None:
            latency = 1000.0

        return PingResult(host, latency, loss, latency < 1000.0)

    except asyncio.TimeoutError:
        return PingResult(host, 1000.0, 100.0, False)
    except Exception as e:
        return PingResult(host, 1000.0, 100.0, False)

async def scan_region(region: str, targets: List[Tuple[str, str]]) -> List[PingResult]:
    """Escaneia todos os alvos de uma região em paralelo."""
    tasks = [async_ping(host) for host, name in targets]
    return await asyncio.gather(*tasks)

async def continuous_pulse(callback, interval: float = 30.0):
    """Loop contínuo de pulso."""
    print(f"[PULSE_NET] Iniciando sensor contínuo (intervalo: {interval}s)")

    while True:
        try:
            all_results = {}
            for region, targets in GLOBAL_TARGETS.items():
                results = await scan_region(region, targets)
                all_results[region] = results

            callback(all_results)
            await asyncio.sleep(interval)
        except Exception as e:
            print(f"[PULSE_NET] Erro: {e}")
            await asyncio.sleep(5)

# Função de integração com Sensorium Core
def create_pulse_callback(sensorium_core):
    def callback(results):
        from sensorium_core import SensorReading
        import time

        for region, pings in results.items():
            for ping in pings:
                if ping.reachable:
                    sensorium_core.add_reading(SensorReading(
                        source=f"pulse_{region}",
                        timestamp=time.time(),
                        metric="latency",
                        value=ping.latency_ms,
                        unit="ms"
                    ))
                sensorium_core.add_reading(SensorReading(
                    source=f"pulse_{region}",
                    timestamp=time.time(),
                    metric="packet_loss",
                    value=ping.packet_loss_pct,
                    unit="%"
                ))

        # Computar gradientes
        for region in results.keys():
            sources = [f"pulse_{region}"]
            gradient = sensorium_core.compute_gradient(region, sources)
            if gradient:
                sensorium_core.log_to_akasha(gradient)

    return callback

if __name__ == "__main__":
    # Teste standalone
    async def test():
        for region, targets in GLOBAL_TARGETS.items():
            results = await scan_region(region, targets)
            print(f"\n[{region}]")
            for r in results:
                status = "✓" if r.reachable else "✗"
                lat = f"{r.latency_ms:.1f}ms" if r.latency_ms < 1000.0 else "TIMEOUT"
                print(f"  {status} {r.target}: {lat} (loss: {r.packet_loss_pct}%)")

    asyncio.run(test())
