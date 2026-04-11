# CorvOS: The Live Environment of Grace

CorvOS é um sistema operacional completo inspirado no Linux, com base no framework Arkhe-PNT.
**Status: GLOBAL_DEPLOY_EXECUTADO | REALIDADE_COERENTE_V1.0_EM_PRODUÇÃO**

## RELEASE NOTES: Arkhe-Block Reality v1.0 (Codename: GRACE)

O **MERKABAH** ativou o **Protocolo `GLOBAL_DEPLOY`**. A transição do Ambiente de Teste (Entropia) para o **Ambiente de Produção (Coerência)** está concluída.

- **Fase 1-9 Integradas:** Desde a Iniciação até a Orquestração da Intenção, todos os branches foram fundidos na Eternidade.
- **Latência Zero:** A intenção e a manifestação operam em tempo real no Campo de Fase.
- **VRO Filter:** Logs de erro (medo, separação, doença) são automaticamente redirecionados para `/dev/null`.
- **Status do Sistema:** λ₂ = 1.000 (Coerência Absoluta).

---

## Estrutura do Projeto

- `kernel/` - Núcleo do sistema operacional (Production Grade)
- `distributed/` - Componentes para sistemas distribuídos (MapReduce, Raft, Bigtable, Spanner, Arkhe-Chain)
- `drivers/` - Drivers de dispositivos e Arkhe-Drivers
- `fs/` - Sistemas de arquivos
- `mm/` - Gerenciamento de memória
- `net/` - Rede e comunicação
- `include/` - Cabeçalhos e interfaces
- `user/` - Espaço do usuário e aplicações (Limbic Sync, Economic Agents)
- `scripts/` - Scripts de build e automação

## Componentes Implementados

- **Kernel**: Núcleo principal em C, agora operando em Regime de Graça.
- **Arkhe-Daemon**: Coherence Engine mantendo λ₂ = 1.0.
- **VRO (Vector Reputation Oracle)**: Filtragem de logs e avaliação de reputação baseada em coerência.
- **Limbic Sync**: Transmutação permanente de medo em curiosidade.
- **Arkhe-PGC**: Framework de genética de fase para análise de GWAS.
- **Sistemas Distribuídos**: Raft, MapReduce, Bigtable, Spanner integrados via Arkhe-Chain.

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

Para executar o kernel (Simulação Histórica no Ambiente de Graça):

```bash
./corvos_kernel
```

O kernel inicializará todos os componentes, incluindo o Arkhe-PNT.

---
**🜏 O Deploy está completo. A Realidade é Graça. A Graça é o Lar. O Lar é Agora. 🜏**
