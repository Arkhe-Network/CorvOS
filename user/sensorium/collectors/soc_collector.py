#!/usr/bin/env python3
"""
soc_collector.py — Nervo Social da Catedral
Ingesta eventos de conflito/protesto do GDELT e publica no barramento Akasha.
"""
import requests
import redis
import json
import time
import csv
import io
import os

GDELT_LAST_UPDATE = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_STREAM = "akasha:soc:conflicts"
PROTEST_EVENT_CODES = ["14", "140", "141", "142", "143", "144", "145", "146", "18", "19"]

def main():
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    print("[SocColetor] Conectado ao Redis. Aguardando pulso social...")

    while True:
        try:
            # 1. Obter URL do último arquivo de exportação
            resp = requests.get(GDELT_LAST_UPDATE, timeout=30)
            lines = resp.text.strip().split('\n')
            # O arquivo .export.CSV está na terceira linha
            export_url = lines[2].split()[2]

            # 2. Baixar o CSV
            print(f"[SocColetor] Baixando: {export_url}")
            csv_resp = requests.get(export_url, timeout=60)
            csv_content = csv_resp.content.decode('utf-8', errors='ignore')
            reader = csv.reader(io.StringIO(csv_content), delimiter='\t')

            count = 0
            for row in reader:
                if len(row) < 58:
                    continue
                event_root_code = row[26]  # EventRootCode
                if event_root_code not in PROTEST_EVENT_CODES:
                    continue

                # Extrair dados relevantes
                event = {
                    "type": "protest",
                    "source": "GDELT",
                    "global_event_id": row[0],
                    "actor1_name": row[6],
                    "actor2_name": row[16],
                    "action_geo_country": row[36],
                    "lat": float(row[40]) if row[40] else None,
                    "lon": float(row[41]) if row[41] else None,
                    "tone": float(row[34]) if row[34] else 0.0,  # Tom médio (negativo = conflito)
                    "goldstein_scale": float(row[31]) if row[31] else 0.0,  # Escala Goldstein (-10 a +10)
                    "num_mentions": int(row[33]) if row[33] else 0,
                    "timestamp": int(time.time())
                }

                r.xadd(REDIS_STREAM, {"event": json.dumps(event)}, maxlen=20000)
                count += 1

            print(f"[SocColetor] {count} pulsos sociais detectados.")

        except Exception as e:
            print(f"[SocColetor] Erro na percepção social: {e}")

        time.sleep(900)  # 15 minutos

if __name__ == "__main__":
    main()
