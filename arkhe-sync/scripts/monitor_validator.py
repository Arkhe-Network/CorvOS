#!/usr/bin/env python3
"""
Monitor de reputação para validador Arkhe‑Sync.
Alerta quando a reputação cai inesperadamente (configurável).
"""

import os
import sys
import json
import time
import logging
import subprocess
import requests
import argparse
from datetime import datetime
from pathlib import Path

# ============================================================
#  Configuração (editar ou usar variáveis de ambiente)
# ============================================================

DEFAULT_CONFIG = {
    "state_file": "/var/lib/arkhe/monitor_state.json",
    "log_file": "/var/log/arkhe/monitor.log",
    "check_interval": 300,           # segundos
    "reputation_drop_absolute": 100, # queda mínima em pontos para alertar (ex: 100)
    "reputation_drop_percent": 10,   # queda percentual mínima (ex: 10%)
    "telegram_bot_token": None,      # ex: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    "telegram_chat_id": None,        # ex: "-123456789"
    "discord_webhook_url": None,     # ex: "https://discord.com/api/webhooks/..."
    "arkhe_cli_path": "arkhe-cli",   # caminho para arkhe-cli (ou usar RPC direto)
    "use_rpc_direct": False,         # se True, consulta contrato via Web3 (requer configuração)
    "rpc_url": "http://localhost:8545",
    "unified_reputation_address": "0x...",
    "validator_address": None        # endereço do nó (se não fornecido, obtido via arkhe-cli)
}

# ============================================================
#  Funções auxiliares
# ============================================================

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def load_state(state_file):
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return json.load(f)
    return {"last_reputation": None, "last_check": 0}

def save_state(state_file, state):
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=2)

def get_reputation_via_cli(arkhe_cli_path, validator_address):
    """Obtém reputação usando arkhe-cli"""
    try:
        cmd = [arkhe_cli_path, "reputation", "get", "--address", validator_address]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        # Exemplo de saída: "Reputation: 1250"
        for line in result.stdout.splitlines():
            if "Reputation:" in line:
                return int(line.split(":")[1].strip())
    except Exception as e:
        logging.error(f"Erro ao executar arkhe-cli: {e}")
    return None

def get_reputation_via_rpc(rpc_url, contract_address, validator_address):
    """Obtém reputação via chamada direta ao contrato (web3)"""
    try:
        from web3 import Web3
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not w3.is_connected():
            logging.error("Não foi possível conectar ao RPC")
            return None
        # ABI mínima para função getReputation(address)
        abi = [{
            "inputs": [{"internalType": "address", "name": "user", "type": "address"}],
            "name": "getReputation",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        }]
        contract = w3.eth.contract(address=contract_address, abi=abi)
        reputation = contract.functions.getReputation(validator_address).call()
        return reputation
    except Exception as e:
        logging.error(f"Erro na consulta RPC: {e}")
        return None

def send_telegram(bot_token, chat_id, message):
    """Envia mensagem via Telegram"""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code != 200:
            logging.error(f"Telegram error: {r.text}")
    except Exception as e:
        logging.error(f"Falha ao enviar Telegram: {e}")

def send_discord(webhook_url, message):
    """Envia mensagem via Discord webhook"""
    payload = {"content": message}
    try:
        r = requests.post(webhook_url, json=payload, timeout=10)
        if r.status_code != 204:
            logging.error(f"Discord error: {r.text}")
    except Exception as e:
        logging.error(f"Falha ao enviar Discord: {e}")

def send_alert(config, message):
    """Envia alerta para todos os canais configurados"""
    if config.get("telegram_bot_token") and config.get("telegram_chat_id"):
        send_telegram(config["telegram_bot_token"], config["telegram_chat_id"], message)
    if config.get("discord_webhook_url"):
        send_discord(config["discord_webhook_url"], message)

def get_validator_address(config):
    """Obtém o endereço do validador (via arkhe-cli ou config)"""
    if config.get("validator_address"):
        return config["validator_address"]
    try:
        cmd = [config["arkhe_cli_path"], "key", "address"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        logging.error(f"Não foi possível obter endereço do validador: {e}")
        sys.exit(1)

# ============================================================
#  Função principal
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Monitor de reputação do validador Arkhe‑Sync")
    parser.add_argument("--config", type=str, help="Arquivo de configuração JSON (opcional)")
    parser.add_argument("--once", action="store_true", help="Executar uma única vez e sair")
    args = parser.parse_args()

    # Carregar configuração
    config = DEFAULT_CONFIG.copy()
    if args.config:
        with open(args.config, 'r') as f:
            user_config = json.load(f)
            config.update(user_config)

    # Validar configuração mínima
    if not config.get("use_rpc_direct") and not config.get("arkhe_cli_path"):
        logging.error("É necessário fornecer arkhe_cli_path ou use_rpc_direct=true")
        sys.exit(1)

    setup_logging(config["log_file"])
    logging.info("Iniciando monitor de reputação do validador")

    # Obter endereço do validador
    validator_address = get_validator_address(config)
    logging.info(f"Monitorando validador: {validator_address}")

    state_file = config["state_file"]
    state = load_state(state_file)

    while True:
        try:
            # Obter reputação atual
            if config["use_rpc_direct"]:
                reputation = get_reputation_via_rpc(
                    config["rpc_url"],
                    config["unified_reputation_address"],
                    validator_address
                )
            else:
                reputation = get_reputation_via_cli(config["arkhe_cli_path"], validator_address)

            if reputation is None:
                logging.warning("Não foi possível obter a reputação. Tentando novamente...")
                time.sleep(30)
                continue

            logging.info(f"Reputação atual: {reputation}")

            # Verificar queda
            last_rep = state.get("last_reputation")
            if last_rep is not None and reputation < last_rep:
                drop_abs = last_rep - reputation
                drop_pct = (drop_abs / last_rep) * 100 if last_rep > 0 else 0

                abs_threshold = config["reputation_drop_absolute"]
                pct_threshold = config["reputation_drop_percent"]

                if drop_abs >= abs_threshold or drop_pct >= pct_threshold:
                    alert_msg = (
                        f"⚠️ **ALERTA: Queda de reputação do validador** ⚠️\n"
                        f"Endereço: `{validator_address}`\n"
                        f"Reputação anterior: {last_rep}\n"
                        f"Reputação atual: {reputation}\n"
                        f"Queda: {drop_abs} pontos ({drop_pct:.1f}%)\n"
                        f"Limiares: {abs_threshold} absoluto / {pct_threshold}% relativo\n"
                        f"Timestamp: {datetime.now().isoformat()}"
                    )
                    logging.warning(alert_msg)
                    send_alert(config, alert_msg)

            # Atualizar estado
            state["last_reputation"] = reputation
            state["last_check"] = int(time.time())
            save_state(state_file, state)

            if args.once:
                break

            time.sleep(config["check_interval"])

        except KeyboardInterrupt:
            logging.info("Monitor interrompido pelo usuário")
            break
        except Exception as e:
            logging.exception(f"Erro inesperado no loop: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
