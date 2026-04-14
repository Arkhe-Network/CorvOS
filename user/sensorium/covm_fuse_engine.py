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
CONSUMER = "fuse_engine_1"

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
        print(f"[FUSE] Erro ao comunicar com daemon: {e}")

def process_event(stream, event_data):
    """Converte um evento bruto em um vetor de fase τ e o envia para o CoPU."""
    try:
        event = json.loads(event_data['event'])
        event_type = event.get('type')
        tau_delta = 0.0

        if event_type == 'earthquake':
            magnitude = event.get('magnitude', 0)
            tau_delta = -0.01 * magnitude

        elif event_type == 'protest':
            # Equação de Tensão Social Refinada (#213-Ω)
            goldstein = event.get('goldstein_scale', 0.0)
            tone = event.get('tone', 0.0)

            if goldstein < -2.0 or tone < -2.0:
                severity = abs(goldstein) * 0.7 + abs(tone) * 0.3
                tau_delta = - (severity / 10.0) * LAMBDA_SOC
                if severity > 5.0:
                    print(f"[FUSE] SOCIAL: Dissonância severa (G={goldstein}, T={tone}) -> Δτ {tau_delta:.4f}")

        elif event_type == 'wildfire':
            # Estresse da Biosfera (#212-Ω)
            frp = event.get('frp', 0)
            confidence = event.get('confidence', 'n')
            # Supondo que o evento possa vir como um cluster ou ponto único
            # Aqui simplificado para o ponto único do fire_collector.py
            tau_delta = - (1.0 ** 1.5) * 0.001 * (frp / 100.0) # Ajustado proporcional ao FRP
            if confidence == 'h':
                tau_delta *= 2.0

        elif event_type == 'energy':
            # Estresse do Metabolismo Carbonífero (#212-Ω)
            carbon = event.get('carbon_intensity', 0)
            tau_delta = - (carbon / 1000.0) * 0.01

        elif event_type == 'vessel':
            tau_delta = 0.0001

        if abs(tau_delta) > 1e-6:
            # Acumular no estado global via Redis
            global_tau_key = "cathedral:global_tau"
            current_tau = float(r.get(global_tau_key) or 0.999)
            new_tau = max(0.1, min(1.0, current_tau + tau_delta))
            r.set(global_tau_key, str(new_tau))

            # Notificar daemon se necessário
            # tune_tau("Global_State", new_tau)

    except Exception as e:
        print(f"[FUSE] Erro processando evento: {e}")

if __name__ == "__main__":
    print(f"[FUSE] Tálamo iniciado. λ_soc={LAMBDA_SOC}. Aguardando eventos...")
    # Initialize global tau if not present
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
