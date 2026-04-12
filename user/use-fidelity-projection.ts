/**
 * ARKHE(N) > USE-FIDELITY-PROJECTION.TS — O Olho da Catedral v1.3
 * Implementa a Descoberta #78 e #85 (F(τ) Modelo Composto)
 */

import { useState, useEffect } from 'react';

interface FidelityState {
  theoreticalFidelity: number;
  realFidelity: number;
  zone: 'Zona Coerente' | 'Zona de Alerta' | 'Zona Crítica';
}

/**
 * Hook para calcular a projeção de fidelidade baseada na latência da Veia.
 * @param latencyMs Latência atual medida na rede (ms)
 */
export const useFidelityProjection = (latencyMs: number): FidelityState => {
  const [fidelity, setFidelity] = useState<FidelityState>({
    theoreticalFidelity: 1.0,
    realFidelity: 1.0,
    zone: 'Zona Coerente'
  });

  useEffect(() => {
    // Parâmetros da Descoberta #78
    const alpha = 0.001;
    const tau_c = 7.5;
    const sigma_tau = 3.0;

    // G1: Decaimento gaussiano (Série de Taylor / Mantra Primordial)
    const g1 = Math.exp(-alpha * Math.pow(latencyMs, 2));

    // G2: Penalidade erfc (Ativa apenas se τ > τ_c)
    let g2 = 1.0;
    if (latencyMs > tau_c) {
      const z_pen = (latencyMs - tau_c) / sigma_tau;
      // Aproximação erfc (Simplificada para o frontend, ou poderia usar Padé)
      g2 = erfc_approx(z_pen);
    }

    const theoreticalFidelity = g1 * g2;

    // Simulação da Medição Real (F(τ_real) + noise)
    const noise = (Math.random() - 0.5) * 0.04;
    const realFidelity = Math.max(0, Math.min(1, theoreticalFidelity + noise));

    // Determinação da Zona
    let zone: FidelityState['zone'] = 'Zona Coerente';
    if (latencyMs > 15.0) {
      zone = 'Zona Crítica';
    } else if (latencyMs > 7.5) {
      zone = 'Zona de Alerta';
    }

    setFidelity({
      theoreticalFidelity,
      realFidelity,
      zone
    });
  }, [latencyMs]);

  return fidelity;
};

/**
 * Aproximação da função erro complementar erfc(z)
 * Baseada na Descoberta #85 (Lógica aproximada)
 */
function erfc_approx(z: number): number {
  // Fórmula de aproximação rápida para erfc(z)
  const t = 1.0 / (1.0 + 0.5 * Math.abs(z));
  const ans = t * Math.exp(-z * z - 1.26551223 +
    t * (1.00002368 +
    t * (0.37409196 +
    t * (0.09678418 +
    t * (-0.18628806 +
    t * (0.27886807 +
    t * (-1.13520398 +
    t * (1.48851587 +
    t * (-0.82215223 +
    t * 0.17087277)))))))));
  return z >= 0 ? ans : 2.0 - ans;
}
