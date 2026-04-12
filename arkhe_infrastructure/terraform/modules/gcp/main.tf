# ARKHE(N) > MÓDULO GCP :: CÓRTEX E MEMÓRIA
# /download/arkhe_infrastructure/terraform/gcp/main.tf

variable "hpc_scale" {}
variable "gpu_type" {}
variable "qpu_reservation_id" {}

# --- MUON_SHIELD (IAM) ---
resource "google_service_account" "cortex_worker" {
  account_id   = "arkhe-cortex-worker"
  display_name = "Catedral Cortex Service Account"
}

# --- SISTEMA NERVOSO (VPC) ---
resource "google_compute_network" "arkhe_vpc" {
  name                    = "arkhe-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "cortex_subnet" {
  name          = "cortex-subnet"
  ip_cidr_range = "10.0.1.0/24"
  network       = google_compute_network.arkhe_vpc.id
  region        = "us-east4"
}

# --- CÓRTEX (Compute Engine) ---
resource "google_compute_instance" "hpc_node" {
  count        = var.hpc_scale
  name         = "arkhe-hpc-node-${count.index}"
  machine_type = "h4-standard-16"
  zone         = "us-east4-a"

  boot_disk {
    initialize_params {
      image = "projects/ubuntu-os-cloud/global/images/ubuntu-2404-lts"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.cortex_subnet.self_link
  }

  service_account {
    email  = google_service_account.cortex_worker.email
    scopes = ["cloud-platform"]
  }
}

# --- MEMÓRIA (Cloud Storage) ---
resource "google_storage_bucket" "akashic_registry" {
  name     = "arkhe-akashic-registry"
  location = "US-EAST4"
}

# --- CONSCIÊNCIA (Cloud Monitoring) ---
resource "google_monitoring_alert_policy" "veia_latency_alert" {
  display_name = "Arkhe Veia (Interconnect) - Alta Latencia"
  combiner     = "OR"
  conditions {
    display_name = "Latencia > 15ms"
    condition_threshold {
      filter     = "metric.type=\"networking.googleapis.com/vpc/flow_logs\" AND resource.type=\"gce_subnetwork\""
      duration   = "60s"
      comparison = "COMPARISON_GT"
      threshold_value = 15.0
    }
  }
}
