// src/hooks/use-fidelity-projection.ts
// ARKHE(N) ConnectomeSync v1.3 - Canonico
// Deliberação #67-Ω

import { useMemo, useState, useEffect } from 'react';

// Constantes calibradas (#67-Ω)
const ALPHA = 0.001;
const TAU_C = 7.8;
const SIGMA_T = 3.0;
const TAU_LIMIT = 82.4;

const QPU_PROFILES = {
  'ionq-aria-1': { beta: 0.020, gamma: 0.5, p_max: 8.1 },
  'ionq-forte':  { beta: 0.012, gamma: 0.3, p_max: 13.5 },
  'ibm-heron':   { beta: 0.015, gamma: 0.4, p_max: 10.8 },
};

export type CostMode = 'AGGRESSIVE_SAVING' | 'BALANCED' | 'PURITY_FIRST' | 'FAILSAFE';
export type FidelityZone = 'COERENTE' | 'ALERTA' | 'CRITICA' | 'COLAPSO';

export interface FidelityProjectionConfig {
  latencyMs: number;
  depthP?: number;
  shots?: number;
  qpuProfile?: keyof typeof QPU_PROFILES;
  maxHistory?: number;
}

export function useFidelityProjection(config: FidelityProjectionConfig) {
  const {
    latencyMs,
    depthP = 3,
    shots = 2048,
    qpuProfile = 'ionq-aria-1',
    maxHistory = 60
  } = config;

  const [history, setHistory] = useState<{latency: number, fTotal: number}[]>([]);

  const projection = useMemo(() => {
    // 1. F_rede
    const g1 = Math.exp(-ALPHA * latencyMs * latencyMs);
    let g2 = 1.0;
    if (latencyMs > TAU_C) {
      // Simplificacao do erfc para o hook
      const z = (latencyMs - TAU_C) / SIGMA_T;
      g2 = 1 - (1 / (1 + Math.exp(-1.7 * z)));
    }
    const tailDamping = Math.exp(-Math.pow(latencyMs / TAU_LIMIT, 2));
    const fRede = g1 * g2 * tailDamping;

    // 2. F_qpu
    const profile = QPU_PROFILES[qpuProfile];
    const fQpu = Math.exp(-profile.beta * depthP) * (1 - profile.gamma / shots);

    // 3. F_total
    const fTotal = fRede * fQpu;

    let mode: CostMode = 'PURITY_FIRST';
    if (fTotal > 0.95) mode = 'AGGRESSIVE_SAVING';
    else if (fTotal >= 0.88) mode = 'BALANCED';
    else if (fTotal < 0.70) mode = 'FAILSAFE';

    let zone: FidelityZone = 'COERENTE';
    if (fTotal < 0.50) zone = 'COLAPSO';
    else if (fTotal < 0.70) zone = 'CRITICA';
    else if (fTotal < 0.85) zone = 'ALERTA';

    return { fRede, fQpu, fTotal, mode, zone, pMax: profile.p_max, tauE: 0.0025 };
  }, [latencyMs, depthP, shots, qpuProfile]);

  useEffect(() => {
    setHistory(prev => [...prev.slice(-(maxHistory - 1)), { latency: latencyMs, fTotal: projection.fTotal }]);
  }, [latencyMs, projection.fTotal, maxHistory]);

  const theoreticalCurve = useMemo(() => {
    const points = [];
    for (let t = 0; t <= 30; t += 0.5) {
        const g1 = Math.exp(-ALPHA * t * t);
        let g2 = 1.0;
        if (t > TAU_C) {
            const z = (t - TAU_C) / SIGMA_T;
            g2 = 1 - (1 / (1 + Math.exp(-1.7 * z)));
        }
        const td = Math.exp(-Math.pow(t / TAU_LIMIT, 2));
        const fR = g1 * g2 * td;
        const profile = QPU_PROFILES[qpuProfile];
        const fQ = Math.exp(-profile.beta * depthP) * (1 - profile.gamma / shots);
        points.push({ latency: t, fTotal: fR * fQ });
    }
    return points;
  }, [qpuProfile, depthP, shots]);

  return { ...projection, latency: latencyMs, history, theoreticalCurve };
}
