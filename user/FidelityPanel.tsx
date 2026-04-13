// ============================================================================
// FidelityPanel.tsx — O Osciloscópio de Fidelidade
// ConnectomeSync v1.3 — Deliberação #67-Ω
// ============================================================================

import React, { useMemo } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ReferenceLine, ResponsiveContainer, Area, ComposedChart
} from 'recharts';
import { useFidelityProjection, type CostMode, type FidelityZone } from './use-fidelity-projection';

const ZONE_COLORS: Record<FidelityZone, string> = {
  COERENTE: '#00f5d4',
  ALERTA:   '#fbbf24',
  CRITICA:  '#ef4444',
  COLAPSO:  '#7f1d1d',
};

const MODE_COLORS: Record<CostMode, string> = {
  AGGRESSIVE_SAVING: '#22c55e',
  BALANCED:          '#3b82f6',
  PURITY_FIRST:      '#f59e0b',
  FAILSAFE:          '#ef4444',
};

const MODE_LABELS: Record<CostMode, string> = {
  AGGRESSIVE_SAVING: 'AGRESSIVO',
  BALANCED:          'EQUILIBRADO',
  PURITY_FIRST:      'PUREZA',
  FAILSAFE:          'FALLBACK',
};

export const FidelityPanel: React.FC = () => {
  const {
    latency, fRede, fQpu, fTotal, mode, zone, tauE,
    history, theoreticalCurve, pMax
  } = useFidelityProjection({
    qpuProfile: 'ionq-aria-1',
    depth: 3,
    shots: 2048,
    costPerShot: 0.149,
    discoveryValue: 63.85,
    updateInterval: 3000,
    maxHistory: 60,
  });

  // Dados do gráfico: curva teórica + medições reais
  const chartData = useMemo(() => {
    // Criar mapa de latência → F_total real para sobrepor
    const realMap = new Map(history.map(h => [h.latency, h.fTotal]));

    return theoreticalCurve.map(point => ({
      latency: point.latency,
      teorico: point.fTotal,
      real: realMap.get(point.latency) ?? null,
    }));
  }, [theoreticalCurve, history]);

  return (
    <div className="bg-slate-900/50 backdrop-blur-md rounded-xl p-6 border border-cyan-500/20 space-y-4 font-mono">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-sm font-bold text-cyan-400 uppercase tracking-wider">
            👁️ Osciloscópio de Fidelidade
          </h2>
          <p className="text-[10px] text-slate-400 mt-1">
            F_total = F_rede(τ) × F_qpu(p, shots)
          </p>
        </div>
        <div className="flex items-center gap-3">
          {/* Indicadores de Modo */}
          {(Object.keys(MODE_COLORS) as CostMode[]).map(m => (
            <div key={m} className="flex items-center gap-1.5">
              <div
                className={`w-2 h-2 rounded-full transition-all duration-500 ${
                  mode === m ? 'animate-pulse scale-125' : 'opacity-20'
                }`}
                style={{ backgroundColor: MODE_COLORS[m] }}
              />
              <span className="text-[8px] text-slate-500">
                {MODE_LABELS[m]}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Métricas Inline */}
      <div className="grid grid-cols-5 gap-3">
        <MetricBadge label="F_rede" value={fRede} color="#00f5d4" />
        <MetricBadge label="F_qpu" value={fQpu} color="#fbbf24" />
        <MetricBadge label="F_total" value={fTotal} color={ZONE_COLORS[zone]} />
        <MetricBadge label="τ_E" value={tauE} color="#3b82f6" />
        <MetricBadge label="p_max" value={pMax} color="#8b5cf6" />
      </div>

      {/* Gráfico Principal */}
      <div className="h-48 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,245,212,0.05)" />
            <XAxis
              dataKey="latency"
              type="number"
              domain={[0, 30]}
              tick={{ fill: '#64748b', fontSize: 8 }}
              tickFormatter={(v: number) => `${v}ms`}
            />
            <YAxis
              domain={[0, 1.05]}
              tick={{ fill: '#64748b', fontSize: 8 }}
              tickFormatter={(v: number) => v.toFixed(1)}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(2, 6, 23, 0.9)',
                border: '1px solid rgba(0, 245, 212, 0.2)',
                fontSize: '10px',
              }}
            />

            {/* Zonas de fundo */}
            <Area
              dataKey="teorico"
              fill="rgba(6, 182, 212, 0.05)"
              stroke="none"
            />

            {/* Curvas */}
            <Line
              type="monotone"
              dataKey="teorico"
              stroke="#fbbf24"
              strokeWidth={2}
              dot={false}
              name="F(τ) Teórica"
            />
            <Line
              type="monotone"
              dataKey="real"
              stroke="#00f5d4"
              strokeWidth={1.5}
              strokeDasharray="5 5"
              dot={false}
              name="Medição Real"
            />

            {/* Linhas de referência */}
            <ReferenceLine y={0.85} stroke="#22c55e" strokeDasharray="3 3" />
            <ReferenceLine x={7.8} stroke="#3b82f6" strokeDasharray="3 3" />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between pt-2 border-t border-white/5">
        <span className="text-[10px] text-slate-500">
          Veia: <span className="text-cyan-400">{latency.toFixed(2)} ms</span>
        </span>
        <span
          className="text-[10px] px-2 py-0.5 rounded-full"
          style={{
            backgroundColor: `${MODE_COLORS[mode]}10`,
            color: MODE_COLORS[mode],
            border: `1px solid ${MODE_COLORS[mode]}30`,
          }}
        >
          {MODE_LABELS[mode]}
        </span>
        <span className="text-[10px] text-slate-500">
          Zona: <span style={{ color: ZONE_COLORS[zone] }}>{zone}</span>
        </span>
      </div>
    </div>
  );
};

// ─── COMPONENTE AUXILIAR ───

function MetricBadge({
  label, value, color
}: {
  label: string;
  value: number;
  color: string;
}) {
  return (
    <div className="bg-black/20 rounded-lg p-2 text-center border border-white/5">
      <div className="text-[7px] text-slate-500 uppercase">{label}</div>
      <div className="text-xs font-bold" style={{ color }}>
        {value.toFixed(3)}
      </div>
    </div>
  );
}
