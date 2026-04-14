# user/sensorium/covm_fuse_engine.py
import redis
import json
import socket
import os
import time

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
SOCKET_PATH = os.getenv("COVM_SOCKET", "/var/run/covm.sock")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
STREAMS = ["akasha:geo:earthquakes", "akasha:mari:vessels", "akasha:soc:conflicts"]
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
        print(f"[FUSE] Erro: Socket {SOCKET_PATH} não encontrado.")
        return

    try:
        cmd = {"op": "swap", "a": cobit_id, "b": cobit_id, "tau": new_tau} # Emulando tune via swap-self se necessário ou use opcode correto se o daemon suportar
        # O daemon atual suporta 'init', 'measure', 'swap', 'ping'.
        # Vamos usar 'init' para atualizar se for o caso ou apenas simular o envio.
        payload = json.dumps({"op": "init", "tau": new_tau, "id": cobit_id}) + "\n"

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.connect(SOCKET_PATH)
        sock.sendall(payload.encode())
        resp = sock.recv(4096)
        sock.close()
        print(f"[FUSE] CoVM Response: {resp.decode().strip()}")
    except Exception as e:
        print(f"[FUSE] Erro ao comunicar com daemon: {e}")

def process_event(stream, event_data):
    """Converte um evento bruto em um vetor de fase τ e o envia para o CoPU."""
    try:
        event = json.loads(event_data['event'])

        # Mapeamento de tipo de evento para ajuste de τ
        tau_delta = 0.0
        if event['type'] == 'earthquake':
            magnitude = event.get('magnitude', 0)
            tau_delta = -0.01 * magnitude  # Terremotos reduzem coerência
        elif event['type'] == 'protest':
            tau_delta = -0.005
        elif event['type'] == 'vessel':
            tau_delta = 0.0001 # Atividade econômica aumenta levemente

        print(f"[FUSE] Stream: {stream} | Evento {event['type']} -> Δτ = {tau_delta}")

        # Aqui assumimos um COBIT "Global_State"
        # tune_tau("Global_State", 0.99 + tau_delta)

    except Exception as e:
        print(f"[FUSE] Erro processando evento: {e}")

if __name__ == "__main__":
    print("[FUSE] Motor de Fusão COVM iniciado. Aguardando eventos...")
    while True:
        try:
            # Ler de todos os streams
            streams_query = {s: '>' for s in STREAMS}
            messages = r.xreadgroup(GROUP, CONSUMER, streams_query, count=10, block=2000)

            if messages:
                for stream, msgs in messages:
                    for msg_id, data in msgs:
                        process_event(stream, data)
                        r.xack(stream, GROUP, msg_id)
        except Exception as e:
            print(f"[FUSE] Loop Erro: {e}")
            time.sleep(5)
