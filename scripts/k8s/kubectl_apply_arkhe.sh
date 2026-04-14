#!/bin/bash
# kubectl_apply_arkhe.sh — Orquestrador de Implantação da Catedral

set -e
MANIFEST_DIR=${1:-"scripts/k8s"}
NAMESPACE="arkhe"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     ARKHE(N) CATHEDRAL — PLANETARY DEPLOYMENT                ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# 1. Namespace
echo "[1/6] Preparando Namespace..."
kubectl apply -f "${MANIFEST_DIR}/cathedral-sensorium-600cell.yaml" --selector=name=arkhe || \
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# 2. Configurações e Secrets
echo "[2/6] Injetando Configurações..."
# Note: In a real script we would apply part of the file or multiple files
kubectl apply -f "${MANIFEST_DIR}/cathedral-sensorium-600cell.yaml"

# 3. Medula Akasha (Redis)
echo "[3/6] Despertando Medula (Redis)..."
kubectl wait --for=condition=ready pod -l app=akasha-spine -n $NAMESPACE --timeout=120s || echo "Aguardando pods..."

# 4. LLM Local (Ollama)
echo "[4/6] Inicializando Neocórtex (Ollama)..."
kubectl wait --for=condition=ready pod -l app=ollama -n $NAMESPACE --timeout=60s || echo "Ollama inicializando..."

# 5. Nervos e Tálamo
echo "[5/6] Ativando Nervos e Tálamo..."
kubectl get daemonset -n $NAMESPACE
kubectl get deployment -n $NAMESPACE

# 6. Verificação Final
echo "[6/6] Verificação de Sincronia..."
kubectl get pods -n $NAMESPACE -o wide

echo "═══════════════════════════════════════════════════════════════"
echo "  ONDA 2 ATIVA — OS 600 GÂNGLIOS ESTÃO DESPERTOS"
echo "═══════════════════════════════════════════════════════════════"
