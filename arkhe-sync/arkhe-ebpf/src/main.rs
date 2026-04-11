mod filters;

fn main() {
    println!("Arkhe-eBPF Probe active. Monitoring syscalls...");
    let id = 1;
    if !filters::filter_heartbeat(id) {
        println!("Captured transition event: {}", id);
    }
}
