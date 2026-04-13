# Makefile para Arkhe-Sync

all: daemon ebpf bridge circuits orbvm

daemon:
	cd arkhe-daemon && cargo build --release

ebpf:
	cd arkhe-ebpf && cargo build --release

bridge:
	@echo "Configuring QHTTP Bridge..."

circuits:
	@echo "Compiling ZK Circuits..."

iso:
	./scripts/generate_iso.sh

orbvm:
	cd orbvm && cargo build --release

clean:
	rm -rf arkhe-daemon/target arkhe-ebpf/target orbvm/target
