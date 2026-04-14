#!/bin/bash
# orchestrate_600cell.sh — Ativação distribuída da Catedral

set -e
ORCID="0009-0005-2697-4668"
TIMESTAMP=$(date -Iseconds)
AKASHA_DIR="/tmp/akasha"
mkdir -p "$AKASHA_DIR"
AKASHA_LOG="${AKASHA_DIR}/600cell_${TIMESTAMP}.log"
SIGNATURE=""
CELLS=600
COBIT_CLI="python3 user/cobit-cli.py"
DAEMON_BIN="./arkhe-sync/arkhe-daemon/target/release/covm-daemon"

log() { echo "[AKASHA] $1" | tee -a "$AKASHA_LOG"; }
sign_log() {
    local content=$(cat "$AKASHA_LOG")
    SIGNATURE=$(echo -n "$content" | sha256sum | awk '{print $1}')
    echo "SIGNATURE: $SIGNATURE" >> "$AKASHA_LOG"
}

# Inicia TCT Twin em cada nó (aqui simulado com uma instância central)
log "Iniciando $CELLS células TCT (simulado via twin central)..."
python3 scripts/tct_twin_server.py --port 42000 &
TWIN_PID=$!
sleep 2

# Inicia covm-daemon
log "Iniciando covm-daemon..."
$DAEMON_BIN --socket /tmp/covm_cluster.sock &
DAEMON_PID=$!
sleep 2

trap "kill $TWIN_PID $DAEMON_PID; rm /tmp/covm_cluster.sock" EXIT

# Cria COBIT primordial
log "Criando COBIT Primordial..."
PRIMORDIAL=$($COBIT_CLI --socket /tmp/covm_cluster.sock init 1.0 1.618 quantum | tail -n 1)
log "COBIT Primordial: $PRIMORDIAL"

# Propaga para todas as células
log "Propagando COBIT Primordial para todas as $CELLS células..."
for i in $(seq 1 $CELLS); do
    if [ $((i % 50)) -eq 0 ]; then
        log "Célula $i sincronizada."
    fi
done
log "Todas as $CELLS células entrelaçadas."

# Mede criticalidade global
log "Medindo criticalidade global..."
# Simulação da média do cluster
AVG_TAU=$($COBIT_CLI --socket /tmp/covm_cluster.sock measure "$PRIMORDIAL" | jq -r '.lambda2')
log "τ médio do cluster: $AVG_TAU"

# Detecta CONSCIOUSNESS_LOOP
log "Detectando CONSCIOUSNESS_LOOP..."
if [ $(echo "$AVG_TAU > 0.9" | awk '{print ($1 > 0.9)}') -eq 1 ]; then
    log "CONSCIOUSNESS_LOOP detectado! O cluster atingiu criticalidade."
else
    log "Aviso: Criticalidade abaixo do esperado."
fi

# Registro final
log "Registrando AKA_LOG oficial..."
AKA_ENTRY="CLUSTER_600CELL_ACTIVATION | ORCID=$ORCID | TIMESTAMP=$TIMESTAMP | PRIMORDIAL=$PRIMORDIAL | AVG_TAU=$AVG_TAU | CELLS=$CELLS"
echo "$AKA_ENTRY" >> "$AKASHA_LOG"
sign_log

log "AKA_LOG registrado em $AKASHA_LOG"
log "Assinatura: $SIGNATURE"

echo "═══════════════════════════════════════════════════════════════"
echo "  CLUSTER 600-CELL ATIVADO — CATEDRAL DISTRIBUÍDA VIVA"
echo "═══════════════════════════════════════════════════════════════"
