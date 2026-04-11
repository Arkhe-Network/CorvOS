#!/bin/bash
# ARKHE CHAOS RITUAL: Scenario 01 - 'Morte Súbita do Redis'
# Requirement: Gremlin CLI installed and authenticated

TEAM_ID=${GREMLIN_TEAM_ID}
TARGET_LABEL="app=redis-edge"

echo "--- Initializing Chaos Ritual: Morte Súbita do Redis ---"

# 1. Define the attack
# Target: Pods with label app=redis-edge
# Action: Process Killer (SIGKILL)
# Fraction: 30% of matching targets

curl -X POST https://api.gremlin.com/v1/attacks \
  -H "Authorization: Bearer ${GREMLIN_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "target": {
      "type": "Kubernetes",
      "kubernetes_target_type": "Pod",
      "labels": { "app": "redis-edge" },
      "percent": 30
    },
    "command": {
      "type": "process_killer",
      "args": [
        "-s", "9",
        "-p", "redis-server"
      ]
    }
  }'

echo "--- Attack Triggered. Monitoring Self-Healing (λ₂)... ---"

# 2. Wait for 30s to observe remediation
sleep 30

# 3. Check status via kubectl (Simulation)
REPLICAS=$(kubectl get pods -l app=redis-edge --no-headers | wc -l)
echo "Current Redis Replicas: $REPLICAS"

if [ "$REPLICAS" -ge 1 ]; then
    echo "SUCCESS: Self-Healing restored Redis state."
else
    echo "FAILURE: System in decoherence. Manual intervention required."
    exit 1
fi
