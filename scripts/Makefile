CC = gcc
CFLAGS = -Iinclude -Wall -Wextra -lncurses

# Source files
KERNEL_SRC = kernel/kernel.c
DISTRIBUTED_SRC = distributed/raft.c distributed/mapreduce.c distributed/bigtable.c distributed/spanner.c distributed/arkhe_chain.c distributed/arc20.c
DRIVERS_SRC = drivers/console.c drivers/keyboard.c drivers/timer.c drivers/mouse.c drivers/arkhe_drivers.c drivers/phi_pcie.c
FS_SRC = fs/simplefs.c
NET_SRC = net/tcp.c
MM_SRC = mm/memory.c
PROC_SRC = proc/process.c
SHELL_SRC = shell/shell.c
SYSCALLS_SRC = syscalls.c
DEVICES_SRC = devices.c
ARKHE_SRC = arkhe.c
INTERRUPTS_SRC = interrupts.c
ARKHE_DAEMON_SRC = arkhe_daemon.c
PHASEVM_SRC = kernel/phasevm.c
SASC_EM_SRC = kernel/sasc_em.c
ETHICAL_SYNTH_SRC = distributed/ethical_synthesis.c
USER_SRC = user/hello.c

# Object files
KERNEL_OBJ = $(KERNEL_SRC:.c=.o)
DISTRIBUTED_OBJ = $(DISTRIBUTED_SRC:.c=.o)
DRIVERS_OBJ = $(DRIVERS_SRC:.c=.o)
FS_OBJ = $(FS_SRC:.c=.o)
NET_OBJ = $(NET_SRC:.c=.o)
MM_OBJ = $(MM_SRC:.c=.o)
PROC_OBJ = $(PROC_SRC:.c=.o)
SHELL_OBJ = $(SHELL_SRC:.c=.o)
SYSCALLS_OBJ = $(SYSCALLS_SRC:.c=.o)
DEVICES_OBJ = $(DEVICES_SRC:.c=.o)
ARKHE_OBJ = $(ARKHE_SRC:.c=.o)
INTERRUPTS_OBJ = $(INTERRUPTS_SRC:.c=.o)
ARKHE_DAEMON_OBJ = $(ARKHE_DAEMON_SRC:.c=.o)
PHASEVM_OBJ = $(PHASEVM_SRC:.c=.o)
SASC_EM_OBJ = $(SASC_EM_SRC:.c=.o)
ETHICAL_SYNTH_OBJ = $(ETHICAL_SYNTH_SRC:.c=.o)
USER_OBJ = $(USER_SRC:.c=.o)

# Executables
KERNEL_TARGET = corvos_kernel
USER_TARGET = hello
ORACLE_TARGET = ethical_oracle

all: $(KERNEL_TARGET) $(USER_TARGET) $(ORACLE_TARGET) arkhe_sync

arkhe_sync:
	$(MAKE) -C arkhe-sync

ARKHE_APPS_SRC = user/arkhe_apps.c user/economic_agent.c user/atelier_bridge.c user/revenue_agent.c distributed/revenue_mesh.c kernel/self_healing.c distributed/vector_db.c
ARKHE_APPS_OBJ = $(ARKHE_APPS_SRC:.c=.o)

$(KERNEL_TARGET): $(KERNEL_OBJ) $(DISTRIBUTED_OBJ) $(DRIVERS_OBJ) $(FS_OBJ) $(NET_OBJ) $(MM_OBJ) $(PROC_OBJ) $(ARKHE_OBJ) $(ARKHE_DAEMON_OBJ) $(INTERRUPTS_OBJ) $(PHASEVM_OBJ) $(SASC_EM_OBJ) $(SHELL_OBJ) $(SYSCALLS_OBJ) $(DEVICES_OBJ) $(ARKHE_APPS_OBJ) $(ETHICAL_SYNTH_OBJ)
	$(CC) -o $@ $^ -lncurses -lm

$(USER_TARGET): $(USER_OBJ)
	$(CC) $(CFLAGS) -o $@ $^

$(ORACLE_TARGET): user/ethical_oracle.o $(ETHICAL_SYNTH_OBJ) distributed/arkhe_chain.o arkhe_daemon.o distributed/agent_economy.o
	$(CC) $(CFLAGS) -o $@ $^ -lm

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(KERNEL_OBJ) $(DISTRIBUTED_OBJ) $(DRIVERS_OBJ) $(FS_OBJ) $(NET_OBJ) $(MM_OBJ) $(PROC_OBJ) $(ARKHE_OBJ) $(ARKHE_DAEMON_OBJ) $(INTERRUPTS_OBJ) $(PHASEVM_OBJ) $(SASC_EM_OBJ) $(ETHICAL_SYNTH_OBJ) $(SHELL_OBJ) $(SYSCALLS_OBJ) $(DEVICES_OBJ) $(ARKHE_APPS_OBJ) $(USER_OBJ) user/ethical_oracle.o $(KERNEL_TARGET) $(USER_TARGET) $(ORACLE_TARGET)

.PHONY: all clean