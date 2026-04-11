use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use tokio::sync::RwLock;
use std::sync::Arc;
use tokio::sync::mpsc;

#[derive(Serialize, Deserialize, Clone, Debug)]
pub enum LeadershipMessage {
    Candidate { task_id: String, coherence: f64, skill_count: u32 },
    LeaderAnnounce { task_id: String, leader_id: String, term: u64 },
    Heartbeat { task_id: String, leader_id: String },
    Ack { task_id: String, follower_id: String },
    TaskResult { task_id: String, hypothesis: String, confidence: f64, node_id: String },
    TaskDecision { task_id: String, decision: String, consensus_reached: bool },
}

#[derive(Clone)]
pub struct SubTask {
    pub id: String,
    pub leader: Option<String>,
    pub term: u64,
    pub last_heartbeat: u64,
}

pub struct LiquidOrchestrator {
    pub tasks: Arc<RwLock<HashMap<String, SubTask>>>,
    pub my_id: String,
}

impl LiquidOrchestrator {
    pub fn new(my_id: String) -> Self {
        Self {
            tasks: Arc::new(RwLock::new(HashMap::new())),
            my_id,
        }
    }

    pub async fn register_task(&self, task_id: String) {
        println!("Registering Liquid Task: {}", task_id);
        let mut tasks = self.tasks.write().await;
        tasks.insert(task_id.clone(), SubTask {
            id: task_id,
            leader: None,
            term: 0,
            last_heartbeat: 0,
        });
    }

    pub async fn handle_message(&self, msg: LeadershipMessage) {
        match msg {
            LeadershipMessage::Candidate { task_id, coherence, skill_count } => {
                println!("Election Candidate for {}: Coherence={:.4}, Skills={}", task_id, coherence, skill_count);
            }
            LeadershipMessage::LeaderAnnounce { task_id, leader_id, term } => {
                println!("Leader for {}: {} (Term {})", task_id, leader_id, term);
                let mut tasks = self.tasks.write().await;
                if let Some(task) = tasks.get_mut(&task_id) {
                    task.leader = Some(leader_id);
                    task.term = term;
                }
            }
            _ => {}
        }
    }
}
