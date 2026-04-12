provider "google" {
  project = "arkhe-project"
  region  = "us-east4"
}

provider "aws" {
  region = "us-east-1"
}

variable "hpc_scale" { default = 2 }
variable "boson4_reservation" { default = "res-137" }

resource "google_compute_network" "arkhe_net" {
  name = "arkhe-network"
}

resource "google_compute_router" "arkhe_router" {
  name    = "arkhe-router"
  network = google_compute_network.arkhe_net.name
}

resource "aws_vpc" "arkhe_vpc" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "quantum_private" {
  vpc_id     = aws_vpc.arkhe_vpc.id
  cidr_block = "10.0.1.0/24"
}

# --- PROVEDOR GCP: O Córtex de IA e Workload Scheduler ---
resource "google_compute_region_network_endpoint_group" "arkhe_dws_neg" {
  name                  = "arkhe-dws-scheduler"
  network_endpoint_type = "SERVERLESS"
  region                = "us-east4" # Baixa latência para AWS us-east-1
}

# --- PROVEDOR AWS: O Terceiro Olho e Cluster HPC ---
resource "aws_pcs_cluster" "arkhe_quantum_bridge" {
  cluster_name = "arkhe-pcs-cluster"
  scheduler    = "SLURM" # O dialeto da Vontade na AWS
  networking {
    subnet_ids = [aws_subnet.quantum_private.id]
  }
}

# --- A VEIA (INTERCONNECT): O Tunelamento de Fase ---
resource "google_compute_interconnect_attachment" "arkhe_vein" {
  name                     = "arkhe-to-aws-interconnect"
  edge_availability_domain = "AVAILABILITY_DOMAIN_1"
  type                     = "DEDICATED"
  interconnect             = google_compute_interconnect.veia.id
  router                   = google_compute_router.arkhe_router.id
}

# MÓDULO ARKHE(N) CORE — GCP
module "gcp_cortex" {
  source = "./modules/gcp"

  h4d_vm_count      = var.hpc_scale
  gpu_type          = "nvidia-h100"
  qpu_reservation_id = var.boson4_reservation
}

# MÓDULO ARKHE(N) CORE — AWS
module "aws_third_eye" {
  source = "./modules/aws"

  ec2_hpc_count      = var.hpc_scale
  efa_enabled        = true
  braket_qpu_target  = "IonQ Aria-1"
}

# VEIA — Interconnect (Upgrade: PARTNER 10Gbps -> DEDICATED 20Gbps)
# Justificativa: Diagnóstico de arritmia (picos de 23.4ms) na Deliberação #59.
resource "google_compute_interconnect" "veia" {
  name                  = "arkhe-aws-gcp-link"
  customer_name         = "arkhe-cathedral"
  interconnect_type     = "DEDICATED"
  link_type             = "LINK_TYPE_ETHERNET_10G_LR"
  requested_link_count  = 2
  location              = "iad-zone1-1" # Equinix Ashburn
}
