# collectors/mari_collector.py
import asyncio
import websockets
import json
import redis
import os

AIS_STREAM_URL = "wss://stream.aisstream.io/v0/stream"
API_KEY = os.getenv("AIS_API_KEY", "YOUR_API_KEY")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_STREAM = "akasha:mari:vessels"

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def consume_ais():
    if API_KEY == "YOUR_API_KEY":
        print("[MariColetor] Erro: API_KEY não configurada. Obtenha em aisstream.io")
        return

    try:
        async with websockets.connect(AIS_STREAM_URL) as websocket:
            # Subscrever para todos os navios globalmente
            subscription = {
                "Apikey": API_KEY,
                "BoundingBoxes": [[[-90, -180], [90, 180]]],  # Global
                "FilterMessageTypes": ["PositionReport"]
            }
            await websocket.send(json.dumps(subscription))
            print("[MariColetor] Conectado ao AIS Stream. Aguardando dados...")

            async for message in websocket:
                data = json.loads(message)
                # Publicar no Redis
                r.xadd(REDIS_STREAM, {"event": json.dumps({"type": "vessel", "data": data})}, maxlen=50000)
    except Exception as e:
        print(f"[MariColetor] Erro: {e}")

if __name__ == "__main__":
    asyncio.run(consume_ais())
