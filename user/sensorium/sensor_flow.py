#!/usr/bin/env python3
"""
sensor_flow.py — Sensor de Fluxo de Rede
Mede largura de banda, RTT e jitter para CDNs e serviços globais.
"""

import asyncio
import aiohttp
import time
from dataclasses import dataclass
from typing import List

FLOW_TARGETS = {
    "cdn_global": [
        ("https://www.google.com", "Google"),
        ("https://www.cloudflare.com", "Cloudflare"),
    ],
    "apis_critical": [
        ("https://api.github.com", "GitHub API"),
    ],
}

@dataclass
class FlowResult:
    target: str
    name: str
    status_code: int
    latency_ms: float
    tls_handshake_ms: float
    content_length: int
    reachable: bool

async def measure_flow(session: aiohttp.ClientSession, url: str, name: str) -> FlowResult:
    """Mede fluxo HTTP para um alvo."""
    start = time.time()
    tls_start = time.time()

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            tls_end = time.time()
            content = await resp.read()
            end = time.time()

            return FlowResult(
                target=url,
                name=name,
                status_code=resp.status,
                latency_ms=(end - start) * 1000,
                tls_handshake_ms=(tls_end - tls_start) * 1000,
                content_length=len(content),
                reachable=True
            )
    except asyncio.TimeoutError:
        return FlowResult(url, name, 0, 10000.0, 0, 0, False)
    except Exception as e:
        return FlowResult(url, name, 0, 10000.0, 0, 0, False)

async def scan_flow_group(group: str, targets: List[tuple]) -> List[FlowResult]:
    """Escaneia grupo de fluxos em paralelo."""
    async with aiohttp.ClientSession() as session:
        tasks = [measure_flow(session, url, name) for url, name in targets]
        return await asyncio.gather(*tasks)

async def continuous_flow(callback, interval: float = 60.0):
    """Loop contínuo de medição de fluxo."""
    print(f"[FLOW_NET] Iniciando sensor de fluxo (intervalo: {interval}s)")

    while True:
        try:
            all_results = {}
            for group, targets in FLOW_TARGETS.items():
                results = await scan_flow_group(group, targets)
                all_results[group] = results

            callback(all_results)
            await asyncio.sleep(interval)
        except Exception as e:
            print(f"[FLOW_NET] Erro: {e}")
            await asyncio.sleep(5)

def create_flow_callback(sensorium_core):
    def callback(results):
        from sensorium_core import SensorReading
        import time

        for group, flows in results.items():
            for flow in flows:
                if flow.reachable:
                    sensorium_core.add_reading(SensorReading(
                        source=f"flow_{group}",
                        timestamp=time.time(),
                        metric="latency",
                        value=flow.latency_ms,
                        unit="ms"
                    ))

        # Computar gradientes por grupo
        for group in results.keys():
            sources = [f"flow_{group}"]
            gradient = sensorium_core.compute_gradient(f"flow_{group}", sources)
            if gradient:
                sensorium_core.log_to_akasha(gradient)

    return callback

if __name__ == "__main__":
    async def test():
        for group, targets in FLOW_TARGETS.items():
            results = await scan_flow_group(group, targets)
            print(f"\n[{group}]")
            for r in results:
                status = f"✓ {r.status_code}" if r.reachable else "✗ ERR"
                lat = f"{r.latency_ms:.0f}ms" if r.latency_ms < 10000.0 else "TIMEOUT"
                print(f"  {status} {r.name}: {lat}")

    asyncio.run(test())
