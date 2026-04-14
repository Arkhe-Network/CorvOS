# collectors/geo_collector.py
import requests
import redis
import json
import time
import os

# Configuração
USGS_FEED_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_STREAM = "akasha:geo:earthquakes"

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def collect_and_publish():
    try:
        response = requests.get(USGS_FEED_URL, timeout=10)
        data = response.json()

        for feature in data['features']:
            props = feature['properties']
            geom = feature['geometry']

            # Normalizar para o formato Akasha
            event = {
                "type": "earthquake",
                "source": "USGS",
                "magnitude": props['mag'],
                "place": props['place'],
                "time": props['time'],
                "coordinates": geom['coordinates'],
                "tsunami": props['tsunami'],
                "alert": props['alert']
            }

            # Publicar no stream do Redis
            r.xadd(REDIS_STREAM, {"event": json.dumps(event)}, maxlen=10000)

        print(f"[GeoColetor] {len(data['features'])} terremotos publicados.")
    except Exception as e:
        print(f"[GeoColetor] Erro: {e}")

if __name__ == "__main__":
    while True:
        collect_and_publish()
        time.sleep(300)  # 5 minutos
