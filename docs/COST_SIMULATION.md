# ARKHE(N) :: SIMULAÇÃO DE CUSTO (MALHA DE VIDRO)

## Estimativa Mensal Consolidada (Deliberação #57)

| COMPONENTE                | TIPO         | CUSTO ESTIMADO       |
| :---                      | :---         | :---                 |
| Interconnect (20 Gbps)    | Dedicado     | $1,500 - 3,000/mês   |
| H4D Cluster (4 nós)       | DWS          | $4,000 - 8,000/mês   |
| EC2 HPC (8 instâncias)    | PCS          | $2,000 - 4,000/mês   |
| Boson 4 (reservado)       | QPU GCP      | $5,000 - 12,000/mês  |
| Braket (500 tarefas/mês)  | QPU AWS      | $150 - 500/mês       |
| Spanner (multi-region)    | Memória      | $500 - 1,500/mês     |
| Aurora PostgreSQL         | Memória      | $300 - 800/mês       |
| FSx for Lustre (1.2 TB)   | HPC Storage  | $200 - 400/mês       |
| Monitoring (CloudWatch)   | Observ.      | $50 - 150/mês        |
| **TOTAL ESTIMADO**        |              | **$14,000 - 31,350/mês** |

## Cenários de Operação (Deliberação #59)

| Cenário                 | Intensidade de Uso      | Custo Total Estimado | τ_E Médio |
| :---                    | :---                    | :---                 | :---      |
| **Monge Copista**       | 1 simulação QAOA/semana | ~$150/mês            | 4.18      |
| **Aprendiz de Feiticeiro**| 1 simulação QAOA/dia    | ~$4.500/mês          | 2.10      |
| **Arquiteto em Transe** | 10 simulações QAOA/dia  | ~$28.000/mês         | 0.95      |

## Otimização Híbrida (DWS ML)
A ativação do `0xF8 ECONOMIC_SHIELD` permite uma economia de até **44.4%** no custo QPU redirecionando ciclos de refinamento para simuladores TPU.
