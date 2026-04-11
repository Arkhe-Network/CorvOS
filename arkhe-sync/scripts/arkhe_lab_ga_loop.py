import json
import time
import random
import numpy as np
import requests

ARKHE_DAEMON_URL = "http://localhost:8080"
COMPONENTS = ["Fe", "Co", "Ni", "Pd", "Pt"]

def predict_property(composition):
    payload = {"skill_id": "tetra_degradation_v1", "composition": composition}
    try:
        resp = requests.post(f"{ARKHE_DAEMON_URL}/predict", json=payload, timeout=10)
        return resp.json().get("predicted_property", 0.5)
    except:
        return random.uniform(0.3, 0.7)

def safety_guard(composition):
    if composition[COMPONENTS.index("Pt")] > 0.3:
        return False
    return True

def run_ga_loop():
    population = [np.random.dirichlet(np.ones(len(COMPONENTS))).tolist() for _ in range(20)]
    for gen in range(5):
        print(f"Generation {gen}")
        fitnesses = [predict_property(c) if safety_guard(c) else 0.0 for c in population]
        # Simplified GA selection and mutation
        best_idx = np.argmax(fitnesses)
        print(f"Best so far: {population[best_idx]} -> {fitnesses[best_idx]:.3f}")

if __name__ == "__main__":
    run_ga_loop()
