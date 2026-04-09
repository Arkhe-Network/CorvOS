#!/bin/bash
# GPU Provisioning Script for Forja Blackwell (QSB Bridge & VRO)
# Target: Ubuntu 22.04 with NVIDIA drivers

echo "--- Initializing Forja Blackwell GPU Cluster ---"

# 1. Update and Install Drivers
sudo apt-get update
sudo apt-get install -y nvidia-driver-535-server nvidia-utils-535-server

# 2. Install Docker & NVIDIA Container Toolkit
sudo apt-get install -y docker.io
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# 3. Pull QSB Pipeline Image
echo "Relaying State: Pulling QSB Pipeline container..."
sudo docker pull arkhe/qsb-pipeline:mainnet-v1.0

# 4. Initialize Local Monitoring
echo "Infrastructure: Setting up Prometheus GPU Exporter..."
sudo docker run -d --name gpu-exporter -p 9445:9445 utkuozdemir/nvidia_gpu_exporter:latest

echo "--- Provisioning Complete. Horizon 3 Ready. ---"
