#!/usr/bin/env python3
"""
energy_collector.py — Nervo Energético da Catedral
Ingesta dados de eletricidade (carbono, renováveis) via Electricity Maps API.
"""
import requests
import redis
import json
import time
import os

API_KEY = os.getenv('EM_API_KEY', 'SUA_CHAVE_AQUI')
BASE_URL = "https://api.electricitymap.org/v3"
ZONES_OF_INTEREST = ["BR-CS", "US-CAL-CISO", "DE", "IN-WE", "ZA", "AUS-NSW"]
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_STREAM = "akasha:infra:energy"

def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    print("[EnergyColetor] Conectado ao Redis. Monitorando o metabolismo elétrico...")

    while True:
        try:
            for zone in ZONES_OF_INTEREST:
                url = f"{BASE_URL}/carbon-intensity/latest?zone={zone}"
                headers = {"auth-token": API_KEY}
                resp = requests.get(url, headers=headers, timeout=30)
                if resp.status_code == 200:
                    data = resp.json()
                    event = {
                        "type": "energy",
                        "source": "ElectricityMaps",
                        "zone": zone,
                        "carbon_intensity": data.get("carbonIntensity", 0),
                        "datetime": data.get("datetime", ""),
                        "renewable_percentage": data.get("renewablePercentage", 0.0)
                    }
                    r.xadd(REDIS_STREAM, {"event": json.dumps(event)}, maxlen=10000)
                    print(f"[EnergyColetor] {zone}: {event['carbon_intensity']} gCO2eq/kWh")
                time.sleep(2)

        except Exception as e:
            print(f"[EnergyColetor] Erro na percepção energética: {e}")

        time.sleep(3600)

if __name__ == "__main__":
    main()
