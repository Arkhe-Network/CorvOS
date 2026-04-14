mod tct_physical;

use clap::Parser;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use tokio::net::{UnixListener, UnixStream};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use uuid::Uuid;
use tct_physical::TCTPhysical;

const TCT_BASE_URL: &str = "http://localhost:42000";

#[derive(Parser)]
#[command(name = "covm-daemon")]
#[command(about = "CoVM Daemon — COBIT Virtual Machine Runtime", long_about = None)]
struct Cli {
    #[arg(short, long, default_value = "/var/run/covm.sock")]
    socket: String,
    #[arg(short, long, default_value = "0.999")]
    baseline_tau: f64,
    #[arg(short, long)]
    tct_device: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Cobit {
    id: String,
    tau: f64,
    phase: f64,
    flavor: String,
    created_at: chrono::DateTime<chrono::Utc>,
}

impl Cobit {
    fn new(tau: f64, phase: f64, flavor: String) -> Self {
        Cobit {
            id: Uuid::new_v4().to_string(),
            tau,
            phase,
            flavor,
            created_at: chrono::Utc::now(),
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
struct Command {
    op: String,
    #[serde(default)]
    id: Option<String>,
    #[serde(default)]
    tau: Option<f64>,
    #[serde(default)]
    phase: Option<f64>,
    #[serde(default)]
    flavor: Option<String>,
    #[serde(default)]
    a: Option<String>,
    #[serde(default)]
    b: Option<String>,
}

#[derive(Debug, Serialize)]
struct Response {
    status: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    id: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    tau: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    phase: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    lambda2: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    message: Option<String>,
}

struct AppState {
    cobits: Mutex<HashMap<String, Cobit>>,
    baseline_tau: f64,
    tct_client: reqwest::Client,
    physical_tct: Option<TCTPhysical>,
}

impl AppState {
    fn new(baseline_tau: f64, tct_device: Option<String>) -> Self {
        let physical_tct = tct_device.and_then(|path| {
            TCTPhysical::open(&path).ok()
        });
        AppState {
            cobits: Mutex::new(HashMap::new()),
            baseline_tau,
            tct_client: reqwest::Client::new(),
            physical_tct,
        }
    }

    async fn tct_request(&self, endpoint: &str, payload: &serde_json::Value) -> Result<serde_json::Value, String> {
        let url = format!("{}/{}", TCT_BASE_URL, endpoint);
        let resp = self.tct_client.post(&url).json(payload).send().await.map_err(|e| e.to_string())?;
        let json = resp.json::<serde_json::Value>().await.map_err(|e| e.to_string())?;
        Ok(json)
    }

    async fn handle_command(&self, cmd: Command) -> Response {
        match cmd.op.as_str() {
            "init" => {
                let tau = cmd.tau.unwrap_or(self.baseline_tau);
                let phase = cmd.phase.unwrap_or(0.0);
                let flavor = cmd.flavor.unwrap_or_else(|| "quantum".to_string());
                let cobit = Cobit::new(tau, phase, flavor);
                let id = cobit.id.clone();
                {
                    let mut map = self.cobits.lock().unwrap();
                    map.insert(id.clone(), cobit);
                }

                if let Some(tct) = &self.physical_tct {
                    tct.set_frequency(4200000000000);
                    tct.set_tau(tau);
                    tct.set_phase(phase);
                    tct.trigger();
                }

                // Notifica TCT Twin
                let payload = serde_json::json!({"op": "init", "id": id, "tau": tau, "phase": phase});
                let _ = self.tct_request("cobit", &payload).await;
                Response { status: "OK".to_string(), id: Some(id), tau: Some(tau), phase: Some(phase), lambda2: None, message: None }
            }
            "measure" => {
                if let Some(id) = cmd.id {
                    let (lambda2_fallback, exists) = {
                        let map = self.cobits.lock().unwrap();
                        if let Some(cobit) = map.get(&id) {
                            (cobit.tau * 0.999, true)
                        } else {
                            (0.0, false)
                        }
                    };

                    if exists {
                        if let Some(tct) = &self.physical_tct {
                            let lambda2 = tct.measure();
                            return Response { status: "OK".to_string(), id: Some(id), tau: None, phase: None, lambda2: Some(lambda2), message: None };
                        }

                        let payload = serde_json::json!({"op": "measure", "id": id});
                        if let Ok(tct_resp) = self.tct_request("measure", &payload).await {
                            if let Some(tct_lambda) = tct_resp.get("lambda2").and_then(|v| v.as_f64()) {
                                return Response { status: "OK".to_string(), id: Some(id), tau: None, phase: None, lambda2: Some(tct_lambda), message: None };
                            }
                        }
                        return Response { status: "OK".to_string(), id: Some(id), tau: None, phase: None, lambda2: Some(lambda2_fallback), message: None };
                    }
                }
                Response { status: "ERROR".to_string(), id: None, tau: None, phase: None, lambda2: None, message: Some("COBIT not found".to_string()) }
            }
            "swap" => {
                if let (Some(a), Some(b)) = (cmd.a, cmd.b) {
                    let result = {
                        let mut map = self.cobits.lock().unwrap();
                        if let (Some(ca), Some(cb)) = (map.get(&a), map.get(&b)) {
                            let new_tau = (ca.tau * cb.tau).sqrt();
                            let new_phase = (ca.phase + cb.phase) / 2.0;

                            if let Some(ca_mut) = map.get_mut(&a) {
                                ca_mut.tau = new_tau;
                                ca_mut.phase = new_phase;
                            }
                            if let Some(cb_mut) = map.get_mut(&b) {
                                cb_mut.tau = new_tau;
                                cb_mut.phase = new_phase;
                            }
                            Some((new_tau, new_phase))
                        } else {
                            None
                        }
                    };

                    if let Some((new_tau, new_phase)) = result {
                        if let Some(tct) = &self.physical_tct {
                            tct.set_tau(new_tau);
                            tct.set_phase(new_phase);
                            tct.trigger();
                        }

                        let payload = serde_json::json!({"op": "swap", "a": a, "b": b});
                        let _ = self.tct_request("swap", &payload).await;
                        return Response { status: "OK".to_string(), id: None, tau: Some(new_tau), phase: Some(new_phase), lambda2: None, message: None };
                    }
                }
                Response { status: "ERROR".to_string(), id: None, tau: None, phase: None, lambda2: None, message: Some("COBIT not found".to_string()) }
            }
            "ping" => {
                match self.tct_request("ping", &serde_json::json!({})).await {
                    Ok(resp) => Response { status: "OK".to_string(), id: None, tau: None, phase: None, lambda2: None, message: Some(format!("TCT: {}", resp)) },
                    Err(e) => Response { status: "ERROR".to_string(), id: None, tau: None, phase: None, lambda2: None, message: Some(e) },
                }
            }
            _ => Response { status: "ERROR".to_string(), id: None, tau: None, phase: None, lambda2: None, message: Some("Unknown op".to_string()) },
        }
    }
}

async fn handle_client(state: Arc<AppState>, stream: UnixStream) {
    let mut reader = BufReader::new(stream);
    let mut line = String::new();
    if reader.read_line(&mut line).await.is_ok() {
        if let Ok(cmd) = serde_json::from_str::<Command>(&line) {
            let resp = state.handle_command(cmd).await;
            let mut writer = reader.into_inner();
            let _ = writer.write_all(serde_json::to_string(&resp).unwrap().as_bytes()).await;
            let _ = writer.write_all(b"\n").await;
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::fmt::init();
    let cli = Cli::parse();
    let _ = std::fs::remove_file(&cli.socket);
    let listener = UnixListener::bind(&cli.socket)?;
    println!("[covm-daemon] Ouvindo em {}, baseline_tau={}", cli.socket, cli.baseline_tau);
    let state = Arc::new(AppState::new(cli.baseline_tau, cli.tct_device));
    loop {
        let (stream, _) = listener.accept().await?;
        let state_clone = state.clone();
        tokio::spawn(async move { handle_client(state_clone, stream).await });
    }
}
