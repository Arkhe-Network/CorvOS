# CorvOS

CorvOS é um sistema operacional completo inspirado no Linux, com base no framework Arkhe-PNT (https://github.com/Arkhe-Network/Arkhe-PNT). Incorpora conceitos avançados de sistemas distribuídos dos seguintes papers:

- [MapReduce: Simplified Data Processing on Large Clusters](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf) - Para processamento paralelo e distribuído de dados.
- [Raft: In Search of an Understandable Consensus Algorithm](https://raft.github.io/raft.pdf) - Para consenso distribuído em redes.
- [Bigtable: A Distributed Storage System for Structured Data](https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf) - Para armazenamento distribuído estruturado.
- [Spanner: Google's Globally-Distributed Database](https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf) - Para bancos de dados distribuídos globalmente.

## Estrutura do Projeto

- `kernel/` - Núcleo do sistema operacional
- `arch/` - Suporte a arquiteturas de hardware
- `drivers/` - Drivers de dispositivos
- `fs/` - Sistemas de arquivos
- `mm/` - Gerenciamento de memória
- `net/` - Rede e comunicação
- `include/` - Cabeçalhos e interfaces
- `lib/` - Bibliotecas compartilhadas
- `scripts/` - Scripts de build e automação
- `user/` - Espaço do usuário e aplicações
- `tools/` - Ferramentas de desenvolvimento
- `distributed/` - Componentes para sistemas distribuídos (MapReduce, Raft, Bigtable, Spanner)

## Componentes Implementados

- **Kernel**: Núcleo principal em C, inspirado no Linux.
- **Gerenciamento de Memória**: Alocação simples de heap.
- **Processos**: Criação, agendamento round-robin com prioridades e context switching com setjmp/longjmp.
- **Interrupções**: Sistema de interrupções simulado com signal handlers.
- **Drivers**:
  - Console: Saída básica.
  - Keyboard: Entrada real usando ncurses.
  - Timer: Temporização com alarm signals.
  - Mouse: Entrada de mouse usando ncurses.
- **Sistema de Arquivos**: SimpleFS, sistema de arquivos em RAM.
- **Rede**: Suporte básico a TCP.
- **Shell**: Interpretador de comandos simples (ls, ps, help, exit).
- **Syscalls**: Interface de system calls básica.
- **Device Manager**: Gerenciamento de dispositivos registrados.
- **Arkhe-PNT**: Integração com o Bio-Quantum Cathedral.
- **Arkhe-PGC**: Framework de genética de fase para análise de GWAS, incluindo LD clumping, coerência global λ₂ (Kuramoto), enriquecimento de vias biológicas (FDR-BH) e coerência cruzada transdiagnóstica com mapeamento funcional eQTL (GTEx/Single-cell).
- **Sistemas Distribuídos**:
  - Raft: Consenso distribuído.
  - MapReduce: Processamento paralelo.
  - Bigtable: Armazenamento estruturado.
  - Spanner: Banco de dados global.

## Como Usar o Shell

Após inicialização, o shell é executado. Comandos disponíveis:
- `ls`: Lista arquivos.
- `ps`: Lista processos.
- `help`: Mostra ajuda.
- `exit`: Sai do shell.

## Como Construir

Para construir o kernel do CorvOS:

```bash
make -f scripts/Makefile
```

Isso compilará o kernel e todos os módulos.

## Como Executar

Para executar o kernel:

```bash
./corvos_kernel
```

O kernel inicializará todos os componentes, incluindo o Arkhe-PNT que iniciará um servidor web na porta 8000.

Nota: O kernel entra em um loop infinito após inicialização. Use Ctrl+C para interromper.
