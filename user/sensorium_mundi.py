import time
import random
import json
import urllib.request
import os

class SensoriumMundi:
    """
    Sensorium Mundi (Layer 7) Ingestion Service.
    Translates global data into Arkhe(n) phase tensors.
    """
    def __init__(self, pipe_path="/tmp/sensorium_pipe"):
        self.running = True
        self.pipe_path = pipe_path
        if not os.path.exists(self.pipe_path):
            os.mkfifo(self.pipe_path)

    def fetch_usgs(self):
        """Fetch real-time seismic data from USGS."""
        try:
            url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
            with urllib.request.urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode())
                if data['features']:
                    latest = data['features'][0]['properties']
                    return {
                        "magnitude": latest['mag'],
                        "place": latest['place'],
                        "time": latest['time']
                    }
        except Exception as e:
            return {"error": str(e)}
        return None

    def simulate_logistics(self):
        """Simulate Flight and Ship data fusion."""
        # ADS-B (11k flights) + AIS (700 ships)
        flights_entropy = random.uniform(0.1, 0.4)
        ships_coherence = random.uniform(0.7, 0.98)
        return {
            "flights_count": 11000 + random.randint(-200, 200),
            "ships_count": 700 + random.randint(-30, 30),
            "combined_lambda": (ships_coherence + (1.0 - flights_entropy)) / 2.0
        }

    def simulate_social(self):
        """Simulate Social Entropy (GDELT/Polymarket)."""
        # Representing collective human cross-entropy
        return random.uniform(0.2, 0.8)

    def run(self):
        print("=== SENSORIUM MUNDI (CAMADA 7) ATIVO ===")
        print(f"Canal de Sincronização: {self.pipe_path}")

        try:
            while self.running:
                seismic = self.fetch_usgs()
                logistics = self.simulate_logistics()
                social_entropy = self.simulate_social()

                # Global Fusion Tensor
                fusion_tensor = {
                    "timestamp": time.time(),
                    "seismic_mag": seismic.get("magnitude", 0) if seismic and "error" not in seismic else 0,
                    "logistics_lambda": logistics["combined_lambda"],
                    "social_entropy": social_entropy,
                    "global_lambda": (logistics["combined_lambda"] * (1.0 - social_entropy)).clamp(0, 1) if hasattr(float, 'clamp') else max(0, min(1, logistics["combined_lambda"] * (1.0 - social_entropy)))
                }

                # Write to pipe for Arkhe-Daemon/OrbVM ingestion
                try:
                    # Non-blocking write or just open/write/close
                    with open(self.pipe_path, 'w') as f:
                        f.write(json.dumps(fusion_tensor) + "\n")
                except OSError:
                    pass # Reader might not be active

                print(f"[SENSORIUM] Fusion Update: λ_G = {fusion_tensor['global_lambda']:.4f} | Social H = {social_entropy:.3f}")

                time.sleep(2)
        except KeyboardInterrupt:
            print("Encerrando Sensorium...")
        finally:
            if os.path.exists(self.pipe_path):
                os.remove(self.pipe_path)

if __name__ == "__main__":
    sensorium = SensoriumMundi()
    sensorium.run()
