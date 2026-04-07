#!/usr/bin/env python3
"""
Arkhe-PGC v4.1: Pathway Coherence, Single-Cell eQTL & Venn Quadrant Analysis.
Comprehensive framework for phase-aware genetic architecture and transdiagnostic overlap.
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_venn import venn2, venn2_circles
import os
import warnings

warnings.filterwarnings('ignore')

class PathwayCoherenceAnalyzer:
    """Calculates internal λ₂ for functional biological pathways."""
    def __init__(self, pathways: dict):
        self.pathways = pathways

    def compute_pathway_internal_coherence(self, df_gwas, snp_to_gene_map):
        results = []
        for name, genes in self.pathways.items():
            pathway_snps = [snp for snp, gene in snp_to_gene_map.items() if gene in genes]
            df_sub = df_gwas[df_gwas['SNP'].isin(pathway_snps)]

            if len(df_sub) >= 3:
                weights = 1.0 / (df_sub['SE'].values**2 + 1e-10)
                theta = np.arctan2(df_sub['BETA'].values, 1.0)
                complex_vecs = np.exp(1j * theta)
                lambda_p = np.abs(np.sum(weights * complex_vecs)) / np.sum(weights)
                results.append({'pathway': name, 'lambda2_internal': lambda_p, 'n_snps': len(df_sub)})

        return pd.DataFrame(results).sort_values('lambda2_internal', ascending=False)

class SingleCellEqtlMapper:
    """Maps SNPs to genes with cell-type resolution (Neuronal, Glial, etc)."""
    def __init__(self):
        self.mapping = {}

    def simulate_mapping(self, snps, cell_type='Neuron'):
        # Mock mapping for simulation
        for snp in snps:
            self.mapping[snp] = f"SC_{cell_type.upper()}_GENE_{snp.replace('rs', '')}"
        return self.mapping

class CrossDisorderAnalyzer:
    """Analyzes overlap and phase alignment between disorders."""
    def __init__(self):
        pass

    def compute_gene_phase_angle(self, gene, snp_to_gene1, snp_to_gene2, df1, df2):
        snps1 = [s for s, g in snp_to_gene1.items() if g == gene]
        snps2 = [s for s, g in snp_to_gene2.items() if g == gene]
        common = set(snps1).intersection(set(snps2))

        if not common: return np.nan

        diff_angles = []
        for snp in common:
            t1 = df1[df1['SNP'] == snp]['theta'].values[0]
            t2 = df2[df2['SNP'] == snp]['theta'].values[0]
            diff = np.angle(np.exp(1j * t1) * np.conj(np.exp(1j * t2)))
            diff_angles.append(np.degrees(diff))
        return np.mean(diff_angles)

    def plot_venn_with_phase(self, set1, set2, gene_phase_angles, title="Overlap", output="user/venn_phase.png"):
        plt.figure(figsize=(8, 8))
        v = venn2([set1, set2], set_labels=('Disorder1', 'Disorder2'))

        if len(gene_phase_angles) > 0:
            avg_angle = np.nanmean(list(gene_phase_angles.values()))
            # Map angle to color: 0 (Green) to 180 (Red)
            norm_angle = np.abs(avg_angle) / 180.0
            cmap = plt.cm.RdYlGn_r # Reverse so green is near 0
            color = cmap(norm_angle)
            if '11' in v.patches:
                v.patches['11'].set_color(color)
                v.patches['11'].set_alpha(0.7)

        plt.title(title)
        plt.savefig(output, dpi=150)
        plt.close()

class ArkhePGC:
    def __init__(self, window_size_bp=250000):
        self.window_size = window_size_bp

    def calculate_metrics(self, df):
        df['weight'] = 1.0 / (df['SE'] ** 2 + 1e-10)
        # Quadrant-aware phase mapping
        df['theta'] = np.arctan2(df['BETA'], 1.0)
        df['complex_vec'] = np.exp(1j * df['theta'])
        return df

    def ld_clumping(self, df):
        df = df.sort_values(by=['CHR', 'weight'], ascending=[True, False])
        pruned = []
        for chrom in df['CHR'].unique():
            chrom_df = df[df['CHR'] == chrom].copy()
            while not chrom_df.empty:
                lead = chrom_df.iloc[0]
                pruned.append(lead)
                mask = (chrom_df['BP'] >= lead['BP'] - self.window_size) & \
                       (chrom_df['BP'] <= lead['BP'] + self.window_size)
                chrom_df = chrom_df[~mask]
        return pd.DataFrame(pruned)

    def compute_coherence(self, df):
        if df.empty: return 0.0
        w = df['weight'].values
        z = df['complex_vec'].values
        return np.abs(np.sum(w * z)) / np.sum(w)

# --- ADVANCED SIMULATION ---

def simulate_gwas_pair(n_snps=5000, seed=42):
    np.random.seed(seed)
    positions = np.sort(np.random.uniform(0, 100e6, n_snps))
    snps = [f'rs{i}' for i in range(n_snps)]

    def gen_df():
        beta = np.random.normal(0, 0.05, n_snps)
        se = np.abs(np.random.normal(0.1, 0.02, n_snps)) + 0.05
        # Shared signal for rs0-rs100
        for i in range(100):
            beta[i] = 0.5 + np.random.normal(0, 0.05)
            se[i] = 0.02
        return pd.DataFrame({'SNP': snps, 'CHR': 1, 'BP': positions.astype(int), 'BETA': beta, 'SE': se})

    return gen_df(), gen_df()

def simulate_realistic_gwas(n_snps=10000, seed=42):
    np.random.seed(seed)
    positions = np.sort(np.random.uniform(0, 100e6, n_snps))
    beta = np.random.normal(0, 0.05, n_snps)
    se = np.abs(np.random.normal(0.1, 0.02, n_snps)) + 0.05
    for i in range(200):
        beta[i] = 0.6 + np.random.normal(0, 0.1)
        se[i] = 0.01
    return pd.DataFrame({'SNP': [f'rs{i}' for i in range(n_snps)], 'CHR': 1, 'BP': positions.astype(int), 'BETA': beta, 'SE': se})
