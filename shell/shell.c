#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../include/keyboard.h"
#include "../include/console.h"
#include "../include/arkhe_daemon.h"
#include "../include/process.h"
#include <unistd.h>
#include "../include/arkhe_chain.h"

// Prototypes for Arkhe apps (simulating separate executables in user space)
void arkhe_fold();
void arkhe_cad();
void arkhe_fem();
void arkhe_music();
void rio_agent_01_run();
void atelier_bridge_formalize_agent(const char *name, const char *soul, const char *dreams);
void example_process();

// Simple Shell for CorvOS
// Command interpreter

void shell_run() {
    char buffer[256];
    while (1) {
        console_write("CorvOS> ");
        int i = 0;
        char c;
        while (1) {
            c = keyboard_read();
            if (c == '\n') break;
            if (c == 0) {
                // No input available, yield to other processes (like the daemon)
                proc_yield();
                // Simulation: periodically inject a command to test functionality
                static int auto_cmd = 0;
                if (++auto_cmd == 10) {
                    strcpy(buffer, "help");
                    i = strlen(buffer);
                    break;
                }
                continue;
            }

            if (c == 127) { // Backspace
                if (i > 0) {
                    i--;
                    console_write("\b \b");
                }
            } else {
                if (i < 255) {
                    buffer[i++] = c;
                    putchar(c);
                }
            }
        }
        buffer[i] = '\0';
        console_writeln("");

        if (strcmp(buffer, "exit") == 0) break;
        else if (strcmp(buffer, "ls") == 0) console_writeln("Files: test.txt");
        else if (strcmp(buffer, "ps") == 0) console_writeln("Processes: kernel, shell");
        else if (strcmp(buffer, "mem") == 0) console_writeln("Memory: 1MB heap");
        else if (strcmp(buffer, "net") == 0) console_writeln("Network: TCP ready");
        else if (strcmp(buffer, "arkhe") == 0) {
            char status[100];
            snprintf(status, 100, "Arkhe: Bio-Quantum Cathedral running (Global Lambda_2: %.3f)", arkhe_get_global_coherence());
            console_writeln(status);
        }
        else if (strcmp(buffer, "urban-sync") == 0) {
            arkhe_daemon_command("urban-sync");
            console_writeln("Urban Sync requested.");
        }
        else if (strcmp(buffer, "run") == 0) {
            proc_create(example_process, 1);
            console_writeln("Process created");
        }
        else if (strcmp(buffer, "fold") == 0) arkhe_fold();
        else if (strcmp(buffer, "cad") == 0) arkhe_cad();
        else if (strcmp(buffer, "fem") == 0) arkhe_fem();
        else if (strcmp(buffer, "music") == 0) arkhe_music();
        else if (strcmp(buffer, "spawn-agent") == 0) rio_agent_01_run();
        else if (strcmp(buffer, "bridge-formalize") == 0) atelier_bridge_formalize_agent("Rio-Agent-01", "SOUL.md", "DREAMS.md");
        else if (strcmp(buffer, "meditate") == 0) {
            arkhe_daemon_command("meditate");
            console_writeln("Meditation mode toggled.");
        }
        else if (strcmp(buffer, "chain-print") == 0) arkhe_chain_print();
        else if (strcmp(buffer, "vm") == 0) {
            console_writeln("VM: Running simple program");
            // Placeholder for VM
        }
        else if (strcmp(buffer, "help") == 0) console_writeln("Commands: ls, ps, mem, net, arkhe, urban-sync, meditate, chain-print, spawn-agent, bridge-formalize, fold, cad, fem, music, run, vm, help, exit");
        else console_writeln("Unknown command");
    }
}