#!/usr/bin/env bash
set -euo pipefail

echo "🜏 Iniciando teste de convergência do enxame Arkhe (3 nós)"
docker build -t arkhe-node:test .
docker-compose up -d
echo "Aguardando propagação da DHT (30s)..."
sleep 30

for node in node_a node_b node_c; do
    echo "--- $node ---"
    docker logs "arkhe_$node" 2>&1 | grep -E "Announcing|swarm running" || echo "Logs not found or mismatch"
done

docker-compose down -v
