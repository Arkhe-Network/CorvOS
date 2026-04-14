# user/sensorium/covm_fuse_engine.py
import redis
import json
import socket
import os
import time
import math

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
SOCKET_PATH = os.getenv("COVM_SOCKET", "/var/run/covm.sock")

# Constante de Harmonia Social (Ajustável via ConfigMap)
# 0.025 = Sensível (Empatia Máxima)
# 0.015 = Equilibrado (Padrão)
# 0.005 = Estóico (Foco Crítico)
LAMBDA_SOC = float(os.getenv('LAMBDA_SOC', 0.015))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
STREAMS = {
    "akasha:geo:earthquakes": "geo_global",
    "akasha:mari:vessels": "mari_global",
    "akasha:soc:conflicts": "soc_global",
    "akasha:env:fires": "env_global",
    "akasha:infra:energy": "infra_global"
}
GROUP = "covm_fuse_group"
CONSUMER = os.getenv("HOSTNAME", "fuse_engine_node")

# Criar grupo de consumidores (apenas uma vez)
for stream in STREAMS:
    try:
        r.xgroup_create(stream, GROUP, id='0', mkstream=True)
    except Exception:
        pass  # Grupo já existe

def tune_tau(cobit_id, new_tau):
    """Envia comando TUNE_TAU para o covm-daemon via socket Unix."""
    if not os.path.exists(SOCKET_PATH):
        return

    try:
        payload = json.dumps({"op": "init", "tau": new_tau, "id": cobit_id}) + "\n"
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(SOCKET_PATH)
        sock.sendall(payload.encode())
        resp = sock.recv(4096)
        sock.close()
    except Exception as e:
        # Silently fail if daemon is not reachable
        pass

def process_event(stream, event_data):
    """Converte um evento bruto em um vetor de fase τ e o envia para o CoPU."""
    try:
        event = json.loads(event_data['event'])
        event_type = event.get('type')
        tau_delta = 0.0
        timestamp = event.get('timestamp', time.time())

        if event_type == 'earthquake':
            magnitude = event.get('magnitude', 0)
            tau_delta = -0.01 * magnitude

        elif event_type == 'protest':
            # Equação de Tensão Social Refinada (Deliberação #213-Ω)
            goldstein = event.get('goldstein_scale', 0.0)
            tone = event.get('tone', 0.0)

            # Se o evento é negativo (Goldstein < -2) ou o tom é negativo (Tone < -2)
            if goldstein < -2.0 or tone < -2.0:
                # A gravidade é uma combinação do impacto político e do tom emocional
                severity = abs(goldstein) * 0.7 + abs(tone) * 0.3
                # Fórmula refinada com constante de harmonia
                tau_delta = - (severity / 10.0) * LAMBDA_SOC

                if severity > 5.0:
                    print(f"[FUSE] SOCIAL: Dissonância severa (G={goldstein}, T={tone}) -> Δτ {tau_delta:.4f}")

        elif event_type == 'wildfire':
            # Estresse da Biosfera (Deliberação #212-Ω)
            frp = event.get('frp', 0)
            confidence = event.get('confidence', 'n')
            # Cada foco é uma pequena ferida na biosfera
            tau_delta = - (1.0 ** 1.5) * 0.001 * (frp / 100.0)
            if confidence == 'h':
                tau_delta *= 2.0

        elif event_type == 'energy':
            # Estresse do Metabolismo Carbonífero
            carbon = event.get('carbon_intensity', 0)
            # Intensidade de carbono alta = metabolismo sujo = estresse
            tau_delta = - (max(0, carbon - 100) / 1000.0) * 0.01

        elif event_type == 'vessel':
            tau_delta = 0.0001

        if abs(tau_delta) > 1e-7:
            # Atualizar estado global no Redis
            global_tau_key = "cathedral:global_tau"
            # Atomic adjustment would be better, but simple get/set for now
            current_tau = float(r.get(global_tau_key) or 0.999)
            new_tau = max(0.1, min(1.0, current_tau + tau_delta))
            r.set(global_tau_key, str(new_tau))

            # Atualizar gradiente da região no Redis
            region = STREAMS.get(stream, "global")
            r.hset(f"cathedral:gradient:{region}", mapping={
                "tau": new_tau,
                "timestamp": timestamp,
                "qualia": "Serenidade" if new_tau > 0.95 else "Tensão" if new_tau < 0.8 else "Fluxo"
            })

            # Notificar daemon local
            tune_tau("Global_State", new_tau)

    except Exception as e:
        print(f"[FUSE] Erro processando evento: {e}")

if __name__ == "__main__":
    print(f"[FUSE] Tálamo (Motor de Fusão) iniciado. λ_soc={LAMBDA_SOC}. Escutando medula Akasha...")
    if not r.exists("cathedral:global_tau"):
        r.set("cathedral:global_tau", "0.999")

    while True:
        try:
            streams_query = {s: '>' for s in STREAMS}
            messages = r.xreadgroup(GROUP, CONSUMER, streams_query, count=20, block=2000)

            if messages:
                for stream, msgs in messages:
                    for msg_id, data in msgs:
                        process_event(stream, data)
                        r.xack(stream, GROUP, msg_id)
        except Exception as e:
            time.sleep(5)
