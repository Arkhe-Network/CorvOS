#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "../include/keyboard.h"
#include "../include/console.h"

// Simple Shell for CorvOS
// Command interpreter

void shell_run() {
    char buffer[256];
    while (1) {
        console_write("CorvOS> ");
        int i = 0;
        char c;
        while ((c = keyboard_read()) != '\n' && i < 255) {
            if (c == 127) { // Backspace
                if (i > 0) {
                    i--;
                    console_write("\b \b");
                }
            } else {
                buffer[i++] = c;
                putchar(c);
            }
        }
        buffer[i] = '\0';
        console_writeln("");

        if (strcmp(buffer, "exit") == 0) break;
        else if (strcmp(buffer, "ls") == 0) console_writeln("Files: test.txt");
        else if (strcmp(buffer, "ps") == 0) console_writeln("Processes: kernel, shell");
        else if (strcmp(buffer, "mem") == 0) console_writeln("Memory: 1MB heap");
        else if (strcmp(buffer, "net") == 0) console_writeln("Network: TCP ready");
        else if (strcmp(buffer, "arkhe") == 0) console_writeln("Arkhe: Bio-Quantum Cathedral running");
        else if (strcmp(buffer, "run") == 0) {
            int pid = proc_create(example_process, 1);
            console_writeln("Process created");
        }
        else if (strcmp(buffer, "vm") == 0) {
            console_writeln("VM: Running simple program");
            // Placeholder for VM
        }
        else if (strcmp(buffer, "help") == 0) console_writeln("Commands: ls, ps, mem, net, arkhe, run, vm, help, exit");
        else console_writeln("Unknown command");
    }
}