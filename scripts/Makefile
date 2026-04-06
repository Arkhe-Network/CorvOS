CC = gcc
CFLAGS = -Iinclude -Wall -Wextra -lncurses

# Source files
KERNEL_SRC = kernel/kernel.c
DISTRIBUTED_SRC = distributed/raft.c distributed/mapreduce.c distributed/bigtable.c distributed/spanner.c
DRIVERS_SRC = drivers/console.c drivers/keyboard.c drivers/timer.c drivers/mouse.c
FS_SRC = fs/simplefs.c
NET_SRC = net/tcp.c
MM_SRC = mm/memory.c
PROC_SRC = proc/process.c
SHELL_SRC = shell/shell.c
SYSCALLS_SRC = syscalls.c
DEVICES_SRC = devices.c
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
USER_OBJ = $(USER_SRC:.c=.o)

# Executables
KERNEL_TARGET = corvos_kernel
USER_TARGET = hello

all: $(KERNEL_TARGET) $(USER_TARGET)

$(KERNEL_TARGET): $(KERNEL_OBJ) $(DISTRIBUTED_OBJ) $(DRIVERS_OBJ) $(FS_OBJ) $(NET_OBJ) $(MM_OBJ) $(PROC_OBJ) $(ARKHE_OBJ) $(INTERRUPTS_OBJ) $(SHELL_OBJ) $(SYSCALLS_OBJ) $(DEVICES_OBJ)
	$(CC) -o $@ $^ -lncurses

$(USER_TARGET): $(USER_OBJ)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(KERNEL_OBJ) $(DISTRIBUTED_OBJ) $(DRIVERS_OBJ) $(FS_OBJ) $(NET_OBJ) $(MM_OBJ) $(PROC_OBJ) $(ARKHE_OBJ) $(INTERRUPTS_OBJ) $(SHELL_OBJ) $(SYSCALLS_OBJ) $(DEVICES_OBJ) $(USER_OBJ) $(KERNEL_TARGET) $(USER_TARGET)

.PHONY: all clean