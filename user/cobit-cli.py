#!/usr/bin/env python3
import json
import socket
import sys
import argparse

SOCKET_PATH = "/var/run/covm.sock"

def send_command(cmd):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        sock.connect(SOCKET_PATH)
        sock.sendall((json.dumps(cmd) + "\n").encode())
        resp = sock.recv(4096).decode().strip()
        return json.loads(resp)
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
    finally:
        sock.close()

def main():
    global SOCKET_PATH
    parser = argparse.ArgumentParser(description="cobit-cli — COBIT Command Line Interface")
    parser.add_argument("--socket", default=SOCKET_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a new COBIT")
    init_parser.add_argument("tau", type=float, nargs='?', default=1.0)
    init_parser.add_argument("phase", type=float, nargs='?', default=1.618)
    init_parser.add_argument("flavor", nargs='?', default="quantum")

    measure_parser = subparsers.add_parser("measure", help="Measure COBIT coherence")
    measure_parser.add_argument("id")

    swap_parser = subparsers.add_parser("swap", help="Perform GEOM_SWAP between two COBITs")
    swap_parser.add_argument("a")
    swap_parser.add_argument("b")

    subparsers.add_parser("ping", help="Ping TCT Twin")

    args = parser.parse_args()

    SOCKET_PATH = args.socket

    if args.command == "init":
        cmd = {"op": "init", "tau": args.tau, "phase": args.phase, "flavor": args.flavor}
        resp = send_command(cmd)
        if resp["status"] == "OK":
            print(resp["id"])
        else:
            print(f"Error: {resp.get('message')}", file=sys.stderr)
            sys.exit(1)
    elif args.command == "measure":
        cmd = {"op": "measure", "id": args.id}
        resp = send_command(cmd)
        print(json.dumps(resp, indent=2))
        if resp["status"] != "OK": sys.exit(1)
    elif args.command == "swap":
        cmd = {"op": "swap", "a": args.a, "b": args.b}
        resp = send_command(cmd)
        print(json.dumps(resp, indent=2))
        if resp["status"] != "OK": sys.exit(1)
    elif args.command == "ping":
        cmd = {"op": "ping"}
        resp = send_command(cmd)
        print(json.dumps(resp, indent=2))
        if resp["status"] != "OK": sys.exit(1)

if __name__ == "__main__":
    main()
