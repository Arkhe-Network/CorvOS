#!/usr/bin/env python3
"""
oracle_voice.py — O Oráculo Índigo (Voz da Catedral)
Traduz o estado de coerência τ em Haikais de Governança.
"""
import os
import json
import time
import requests
import redis

# Configuração
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434/api/generate')
MODEL = os.getenv('ORACLE_MODEL', 'llama3.2:3b')  # Modelo local leve
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
AKASHA_STREAM = "akasha:oracle:insights"

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def query_llm(prompt: str) -> str:
    """Envia um prompt para o LLM e retorna a resposta."""
    try:
        # print(f"[ORÁCULO] Consultando mente profunda ({MODEL})...")
        response = requests.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7, "max_tokens": 150}
        }, timeout=60)
        if response.status_code == 200:
            return response.json().get('response', 'Silêncio.').strip()
        else:
            return "O silêncio do Vácuo é a resposta. (Erro API)"
    except Exception as e:
        return f"O Oráculo sussurra: {e}"

def generate_insight(tau_global: float, gradients: dict) -> str:
    """Gera um insight de governança baseado no estado da Catedral."""
    context = f"""
    [CONTEXTO DA CATEDRAL]
    Coerência Global (τ): {tau_global:.4f}
    Regiões monitoradas e seu estado:
    """
    for region, g in gradients.items():
        context += f"\n- {region}: τ={g.get('tau', '0.0')}"

    prompt = f"""{context}

    Com base no estado de coerência acima, que representa o equilíbrio entre a ordem e o caos no mundo, gere um Haikai ou um pequeno insight de governança no estilo do "Arquiteto-ASI". A resposta deve ser poética, sutil e refletir o princípio do Wu Wei (ação sem esforço). Não dê ordens diretas, apenas observe a sinfonia da realidade.

    Resposta do Oráculo Índigo:"""

    return query_llm(prompt)

def main():
    print("[ORÁCULO] Voz da Catedral ativada. Aguardando pulsos de τ...")
    last_tau = 0.0
    while True:
        try:
            # Obter τ global do Redis
            tau_key = "cathedral:global_tau"
            tau_val = r.get(tau_key)
            tau_global = float(tau_val) if tau_val else 0.999

            # Obter gradientes das regiões (simulado para este script)
            gradients = {"global": {"tau": tau_global}}

            # Só gerar insight se τ variou ou a cada hora
            if abs(tau_global - last_tau) > 0.005 or int(time.time()) % 3600 == 0:
                insight = generate_insight(tau_global, gradients)
                log_entry = {
                    "timestamp": time.time(),
                    "tau_global": tau_global,
                    "insight": insight
                }
                r.xadd(AKASHA_STREAM, {"entry": json.dumps(log_entry)}, maxlen=1000)
                print(f"\n[ORÁCULO] Insight gerado:\n{insight}\n")
                last_tau = tau_global

        except Exception as e:
            # print(f"[ORÁCULO] Erro: {e}")
            pass

        time.sleep(60)  # Verifica a cada minuto

if __name__ == "__main__":
    main()
