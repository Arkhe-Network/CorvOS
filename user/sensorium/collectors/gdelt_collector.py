# collectors/gdelt_collector.py
import requests
import csv
import redis
import time
import os
import io
from datetime import datetime

GDELT_LAST_UPDATE = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_STREAM = "akasha:soc:conflicts"

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def download_latest_gdelt():
    try:
        # Obter URL do último arquivo
        resp = requests.get(GDELT_LAST_UPDATE, timeout=10)
        lines = resp.text.strip().split('\n')
        export_url = lines[2].split()[2]  # URL do arquivo export.CSV

        # Baixar e processar
        print(f"[GDELT] Baixando: {export_url}")
        csv_resp = requests.get(export_url, timeout=30)
        # GDELT CSV can be large, use io.StringIO
        csv_content = io.StringIO(csv_resp.text)
        reader = csv.reader(csv_content, delimiter='\t')

        count = 0
        for row in reader:
            if len(row) < 27:
                continue
            event_code = row[26]  # EventCode
            # Filtrar apenas protestos (código 14*)
            if event_code.startswith('14'):
                event = {
                    "type": "protest",
                    "source": "GDELT",
                    "global_event_id": row[0],
                    "actor1": row[6],
                    "actor2": row[16],
                    "location": row[36],
                    "lat": float(row[40]) if row[40] else None,
                    "lon": float(row[41]) if row[41] else None,
                    "tone": float(row[34]) if row[34] else 0.0
                }
                r.xadd(REDIS_STREAM, {"event": json.dumps(event)}, maxlen=20000)
                count += 1
        print(f"[GDELT] {count} eventos de protesto publicados.")
    except Exception as e:
        print(f"[GDELT] Erro: {e}")

if __name__ == "__main__":
    while True:
        download_latest_gdelt()
        time.sleep(900)  # 15 minutos
