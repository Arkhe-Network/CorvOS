#!/usr/bin/env python3
# tct_twin_server.py — Simulador do TCT que recebe comandos via socket
import socket
import json
import math
import time
import argparse

PHI = (1 + math.sqrt(5)) / 2
TCT_FREQ = 4.20e12

class TCTDigitalTwin:
    def __init__(self):
        self.cobits = {}
        self.tau_environment = 0.9998

    def handle_command(self, cmd):
        if cmd['op'] == 'init':
            cobit_id = cmd.get('id', f"cobit_tct_{len(self.cobits)}")
            tau = cmd.get('tau', 1.0)
            phase = cmd.get('phase', 0.0)
            self.cobits[cobit_id] = {'tau': tau, 'phase': phase}
            return {'status': 'OK', 'id': cobit_id, 'tau': tau}

        elif cmd['op'] == 'swap':
            a, b = cmd['a'], cmd['b']
            if a not in self.cobits or b not in self.cobits:
                return {'status': 'ERROR', 'message': 'COBIT not found'}
            ca, cb = self.cobits[a], self.cobits[b]
            new_tau = math.sqrt(ca['tau'] * cb['tau'])
            new_phase = (ca['phase'] + cb['phase']) / 2.0
            ca['tau'] = cb['tau'] = new_tau
            ca['phase'] = cb['phase'] = new_phase
            return {'status': 'OK', 'tau': new_tau, 'phase': new_phase}

        elif cmd['op'] == 'measure':
            cobit_id = cmd['id']
            if cobit_id not in self.cobits:
                return {'status': 'ERROR', 'message': 'COBIT not found'}
            c = self.cobits[cobit_id]
            lambda2 = c['tau'] * 0.999
            return {'status': 'OK', 'lambda2': lambda2}

        elif cmd['op'] == 'ping':
            return {'status': 'OK', 'message': 'PONG', 'freq': TCT_FREQ}

        return {'status': 'ERROR', 'message': 'Unknown command'}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=42000)
    args = parser.parse_args()

    twin = TCTDigitalTwin()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', args.port))
    sock.listen(5)
    print(f"[TCT Twin] Ouvindo na porta {args.port} (freq={TCT_FREQ/1e12:.2f} THz)")

    while True:
        conn, addr = sock.accept()
        try:
            data = conn.recv(4096).decode()
            if not data:
                conn.close()
                continue
            cmd = json.loads(data)
            print(f"[TCT Twin] Comando recebido: {cmd}")
            response = twin.handle_command(cmd)
            conn.send(json.dumps(response).encode())
        except Exception as e:
            print(f"[TCT Twin] Erro: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    main()
