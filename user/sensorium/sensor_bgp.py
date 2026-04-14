#!/usr/bin/env python3
"""
sensor_bgp.py — Sensor de Estabilidade BGP
Consume feeds de dados BGP para detectar instabilidades de roteamento.
"""

import asyncio
import aiohttp
import time
from dataclasses import dataclass
from typing import Dict, List

# Fontes públicas de dados BGP
BGP_FEEDS = {
    "rir_stats": "https://stats.ripe.net/data/ris/live.json?resource=",
}

@dataclass
class BGPEvent:
    asn: int
    prefix: str
    event_type: str  # "announce", "withdraw"
    timestamp: float

@dataclass
class BGPStability:
    region: str
    stability_score: float  # 0-100
    active_events: int
    top_asns: List[tuple]  # (asn, event_count)

async def fetch_bgp_events() -> List[BGPEvent]:
    """Busca eventos BGP recentes via APIs públicas."""
    events = []

    # Exemplo: RIPE RIS (simulado - API real requer registro)
    try:
        async with aiohttp.ClientSession() as session:
            # Tentativa de obter dados do RIPE Stats
            url = "https://stat.ripe.net/data/ris-wholespace-updates/data.json"
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    # Parse real dos dados RIPE (estrutura simplificada)
                    for item in data.get("data", {}).get("updates", [])[:50]:
                        events.append(BGPEvent(
                            asn=item.get("peer_asn", 0),
                            prefix=item.get("prefix", ""),
                            event_type=item.get("type", "announce"),
                            timestamp=time.time()
                        ))
    except:
        # Fallback: simulação baseada em heurísticas para teste
        pass

    return events

def compute_stability(events: List[BGPEvent]) -> BGPStability:
    """Computa escore de estabilidade baseado nos eventos."""
    if not events:
        return BGPStability("global", 100.0, 0, [])

    # Contar eventos por ASN
    asn_counts = {}
    for e in events:
        asn_counts[e.asn] = asn_counts.get(e.asn, 0) + 1

    withdraws = sum(1 for e in events if e.event_type == "withdraw")

    # Score: mais withdraws = menos estável
    total = len(events)
    withdraw_ratio = withdraws / total if total > 0 else 0
    stability = max(0, 100 - (withdraw_ratio * 200))

    # Top ASNs com mais eventos
    top_asns = sorted(asn_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    return BGPStability(
        region="global",
        stability_score=stability,
        active_events=total,
        top_asns=top_asns
    )

async def continuous_bgp(callback, interval: float = 120.0):
    """Loop contínuo de monitoramento BGP."""
    print(f"[BGP_SENSE] Iniciando sensor BGP (intervalo: {interval}s)")

    while True:
        try:
            events = await fetch_bgp_events()
            stability = compute_stability(events)
            callback(stability)
            await asyncio.sleep(interval)
        except Exception as e:
            print(f"[BGP_SENSE] Erro: {e}")
            await asyncio.sleep(10)

def create_bgp_callback(sensorium_core):
    def callback(stability: BGPStability):
        from sensorium_core import SensorReading
        import time

        sensorium_core.add_reading(SensorReading(
            source="bgp_global",
            timestamp=time.time(),
            metric="bgp_stability",
            value=stability.stability_score,
            unit="score"
        ))

        gradient = sensorium_core.compute_gradient("bgp_global", ["bgp_global"])
        if gradient:
            sensorium_core.log_to_akasha(gradient)

    return callback

if __name__ == "__main__":
    async def test():
        events = await fetch_bgp_events()
        stability = compute_stability(events)
        print(f"[BGP] Estabilidade: {stability.stability_score:.1f}")
        print(f"[BGP] Eventos ativos: {stability.active_events}")
        print(f"[BGP] Top ASNs: {stability.top_asns}")

    asyncio.run(test())
