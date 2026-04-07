#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "raft.h"
#include "mapreduce.h"
#include "bigtable.h"
#include "spanner.h"
#include "arkhe_chain.h"
#include "console.h"
#include "simplefs.h"
#include "tcp.h"
#include "arkhe.h"
#include "arkhe_daemon.h"
#include "memory.h"
#include "process.h"
#include "keyboard.h"
#include "timer.h"
#include "shell.h"
#include "syscalls.h"
#include "devices.h"
#include "arkhe_drivers.h"
#include "phi_pcie.h"

// CorvOS Kernel Entry Point
// Inspirado em Linux, com extensões para sistemas distribuídos baseados em Arkhe-PNT

RaftNode raft_node;
BigtableTable bigtable;
SpannerDB spanner_db;

void kernel_init() {
    printf("CorvOS Kernel Initializing...\n");
    console_init();
    mm_init();
    proc_init();
    keyboard_init();
    timer_init();
    mouse_init();
    interrupts_init();
    register_arkhe_drivers();
    phi_pcie_init();
    device_init_all();
    // Register devices
    device_register("console", console_init, NULL, NULL);
    device_register("keyboard", keyboard_init, NULL, NULL);
    fs_init();
    net_init();
    arkhe_init();
    arkhe_daemon_init();
    arkhe_chain_init();
    raft_init(&raft_node);
    bigtable_init(&bigtable);
    spanner_init(&spanner_db);
    printf("All components initialized\n");
}

void example_process() {
    printf("Example process running\n");
    proc_yield();  // Yield to scheduler
    printf("Back in process\n");
}

void kernel_main() {
    printf("CorvOS Kernel Running...\n");
    // Exemplo de uso dos componentes
    console_writeln("Console test");
    int fd = fs_create("test.txt");
    fs_write(fd, "Hello FS", 8);
    char buffer[100];
    fs_read(fd, buffer, 8);
    console_writeln(buffer);

    // Memory test
    void *ptr = mm_alloc(100);
    printf("Allocated memory at %p\n", ptr);
    mm_free(ptr);

    // Process test
    int pid = proc_create(example_process, 1);
    printf("Created process %d\n", pid);

    // Timer alarm
    timer_set_alarm(5);

    // Arkhe run
    arkhe_run();

    raft_run(&raft_node);
    mapreduce_execute("example input", example_map, example_reduce);
    bigtable_put(&bigtable, "row1", "cf1", "cq1", "value1");
    char *val = bigtable_get(&bigtable, "row1", "cf1", "cq1");
    console_writeln(val);
    spanner_write(&spanner_db, "key1", "value1");
    char *sval = spanner_read(&spanner_db, "key1");
    console_writeln(sval);

    // Loop principal do kernel
    proc_create(shell_run, 1);
    while (1) {
       arkhe_daemon_run();
       proc_schedule();
       timer_delay(100);  // Simple delay
    }
}

int main() {
    kernel_init();
    kernel_main();
    keyboard_close();
    return 0;
}