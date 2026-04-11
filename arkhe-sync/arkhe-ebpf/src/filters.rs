pub fn filter_heartbeat(syscall_id: u32) -> bool {
    // Ignore common heartbeat syscalls
    match syscall_id {
        201 => true, // gettimeofday
        _ => false,
    }
}
