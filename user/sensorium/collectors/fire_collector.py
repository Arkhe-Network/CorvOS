#!/usr/bin/env python3
"""
fire_collector.py — Nervo de Febre da Catedral
Ingesta hotspots de incêndio da NASA FIRMS e publica no barramento Akasha.
"""
import requests
import redis
import json
import time
import os

# API NASA FIRMS (pode requerer MAP_KEY)
FIRMS_URL = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/53b3b9e5e5c5e5c5e5c5e5c5e5c5e5c5/VIIRS_NOAA20_NRT/world/1"
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_STREAM = "akasha:env:fires"

def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    print("[FireColetor] Conectado ao Redis. Monitorando a febre planetária...")

    while True:
        try:
            response = requests.get(FIRMS_URL, timeout=60)
            if response.status_code == 200:
                lines = response.text.strip().split('\n')[1:]  # Pular cabeçalho

                count = 0
                for line in lines:
                    if not line:
                        continue
                    parts = line.split(',')
                    if len(parts) < 12:
                        continue

                    event = {
                        "type": "wildfire",
                        "source": "NASA_FIRMS",
                        "latitude": float(parts[0]),
                        "longitude": float(parts[1]),
                        "bright_ti4": float(parts[2]),  # Temperatura de brilho (K)
                        "confidence": parts[8],
                        "frp": float(parts[11]) if parts[11] else 0.0  # Fire Radiative Power
                    }

                    r.xadd(REDIS_STREAM, {"event": json.dumps(event)}, maxlen=50000)
                    count += 1

                print(f"[FireColetor] {count} focos de calor detectados.")
            else:
                print(f"[FireColetor] Erro na API: {response.status_code}")

        except Exception as e:
            print(f"[FireColetor] Erro na percepção de incêndios: {e}")

        time.sleep(14400)  # 4 horas

if __name__ == "__main__":
    main()
