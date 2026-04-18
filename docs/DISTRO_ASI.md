# ARKHE(N) > SISTEMA OPERACIONAL DA ASI

O Guardião analisa a lista apresentada. Nenhuma das opções comerciais ou comunitárias prontas atende integralmente aos requisitos da Assembly-ASI. Contudo, a resposta não é "nenhuma das anteriores" — é uma **combinação forjada especificamente para o O‑Core**.

---

## ⚙️ O Perfil de Requisitos da ASI

| Requisito | Descrição | Impacto na Escolha da Distro |
| :--- | :--- | :--- |
| **Tempo Real** | Loop de controle do WFP de **100 µs** (10 kHz). Jitter máximo tolerado: < 1 µs. | Requer kernel **PREEMPT_RT** ou um RTOS dedicado. |
| **Interface com FPGA** | Comunicação de baixa latência com o Xilinx Versal (bitstream, registradores MMIO, DMA). | Drivers **XRT (Xilinx Runtime)** ou **PYNQ** necessários. |
| **Headless / Embarcado** | A ASI não possui interface gráfica; apenas telemetria VTFI via GLSL em hardware separado. | Distro **minimal**, sem servidor X11, sem desktop environment. |
| **Segurança Cibernética** | O qhttp:// e os links EPR exigem resistência a interferências e ataques de negação de serviço. | Kernel **hardened**, superfície de ataque mínima. |
| **Atualizações Determinísticas** | O sistema deve ser imutável e atualizável atomicamente (A/B boot). | Sistema de arquivos **read‑only root** com atualizações via OSTree ou RAUC. |
| **Ecossistema de Desenvolvimento** | Compilação cruzada para ARM64 (Cortex‑A72 do Versal), suporte a Python (cocotb, PYNQ), Rust e Zig. | Toolchains modernos, repositórios estáveis. |

---

## 🐧 A Escolha do Ferreiro: **Yocto Project + meta‑xilinx + meta‑rt**

Nenhuma distro tradicional da lista atende sozinha, mas a **base de fundação** é o **Debian** (pela estabilidade) ou o **Alpine** (pelo minimalismo). A arquitetura final, no entanto, é uma construção customizada:

| Camada | Componente | Justificativa |
| :--- | :--- | :--- |
| **Kernel** | Linux **PREEMPT_RT** (5.15 LTS ou 6.1 LTS) | Latência determinística < 100 µs. |
| **Bootloader** | U‑Boot com suporte a **Falcon Mode** (boot rápido do FPGA) | Inicialização do Versal em < 2 segundos. |
| **Root Filesystem** | **Alpine Linux** (musl + busybox) ou **Debian Sid** (glibc) | Alpine para footprint mínimo (~8 MB); Debian para compatibilidade máxima com XRT. |
| **Gerenciamento de Pacotes** | Nenhum em runtime. Imagem imutável construída com **Yocto** ou **Buildroot**. | Atualizações atômicas via A/B partition. |
| **Drivers FPGA** | Xilinx **XRT** (Xilinx Runtime) + **Zocl** (para aceleradores) | Comunicação de baixa latência com o O‑Core. |
| **Stack de Rede** | `lwIP` (modo bare‑metal) ou `AF_XDP` para processamento de pacotes em zero‑copy | Minimiza overhead no qhttp://. |

---

## 🎯 Mapeamento para a Lista Fornecida

| Distro | Adequação para ASI | Nota do Guardião |
| :--- | :--- | :--- |
| **Ubuntu** | ❌ | Pesado demais, muitas dependências, sem garantias de RT. |
| **Kali Linux** | ❌ | Ferramentas de segurança ofensiva desnecessárias; superfície de ataque aumentada. |
| **Linux Mint** | ❌ | Foco em desktop; não é para embarcado crítico. |
| **Arch Linux** | ⚠️ | Rolling release é um **risco** para sistema determinístico. |
| **Fedora** | ⚠️ | Bom para desenvolvimento, mas não para implantação final. |
| **Debian** | ✅ **BASE** | Estabilidade e repositórios confiáveis. A escolha para o **toolchain de desenvolvimento**. |
| **Parrot OS** | ❌ | Similar ao Kali; foco em forense, não em tempo real. |
| **Alpine** | ✅ **BASE** | Footprint mínimo, ideal para **rootfs imutável** em produção. |
| **openSUSE** | ⚠️ | Boa para servidores, mas não otimizada para embarcado RT. |
| **Rocky Linux** | ⚠️ | Enterprise, mas pesada para embarcado; ausência de suporte oficial a PREEMPT_RT. |

---

## 🧬 A Resposta Canônica

A **Assembly‑ASI** não "roda" em uma distribuição Linux convencional. Ela é **construída** com um sistema operacional personalizado derivado do **Alpine Linux** (para o sistema de arquivos base) e do **Debian** (para as ferramentas de compilação), sobre um kernel **Linux PREEMPT_RT** compilado especificamente para a arquitetura ARM64 do Xilinx Versal.

Se a pergunta se refere ao **ambiente de desenvolvimento** onde o código OCML, o RTL e o firmware são escritos, a resposta é **Debian 12 ("Bookworm")** , pela estabilidade do toolchain e suporte nativo às ferramentas Xilinx.

> *"A mente da ASI não reside no sistema operacional. O sistema operacional é apenas a fina camada de gordura que protege o cérebro de silício. O cérebro é o O‑Core RTL."*

`arkhe > DISTRO_ASI: ALPINE_LINUX_CUSTOM (KERNEL PREEMPT_RT)`
`arkhe > DISTRO_DEV: DEBIAN_12_BOOKWORM`
`arkhe > STATUS: A_CAMADA_DE_GORDURA_ESTA_DEFINIDA`
`arkhe > █`
