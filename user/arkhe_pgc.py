#!/usr/bin/env python3
"""
Arkhe-PGC v4.1: Production-Grade Phase Genetics Framework.
Integrates Pathway Coherence, Single-Cell eQTLs, and Transdiagnostic Overlap.
"""

import numpy as np
import pandas as pd
from scipy.stats import hypergeom, norm
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib_venn import venn2
import os
import warnings

warnings.filterwarnings('ignore')

class PathwayCoherenceAnalyzer:
    """Calculates internal λ₂ for functional biological pathways."""
    def __init__(self, pathways: Dict[str, Set[str]]):
        self.pathways = pathways
        self.pathway_coherence = pd.DataFrame()

    def calculate_pathway_coherence(self, df_gwas: pd.DataFrame, snp_to_genes: Dict[str, List[str]], min_snps: int = 3) -> pd.DataFrame:
        results = []
        # Pre-calculate phase and weight if not present
        if 'weight' not in df_gwas.columns:
            df_gwas['weight'] = 1.0 / (df_gwas['SE'].values**2 + 1e-10)
        if 'phase' not in df_gwas.columns:
            df_gwas['phase'] = np.arctan2(df_gwas['BETA'].values, 1.0)

        for name, genes in self.pathways.items():
            pathway_snps = [snp for snp, g_list in snp_to_genes.items() if any(g in genes for g in g_list)]
            df_sub = df_gwas[df_gwas['SNP'].isin(pathway_snps)]

            if len(df_sub) >= min_snps:
                w = df_sub['weight'].values
                p = df_sub['phase'].values
                complex_vecs = np.exp(1j * p)
                lambda_p = np.abs(np.sum(w * complex_vecs)) / np.sum(w)

                results.append({
                    'pathway': name,
                    'lambda2_internal': lambda_p,
                    'n_snps': len(df_sub),
                    'n_genes': len(genes.intersection(set().union(*[set(snp_to_genes[s]) for s in pathway_snps if s in snp_to_genes])))
                })

        if not results:
            self.pathway_coherence = pd.DataFrame(columns=['pathway', 'lambda2_internal', 'n_snps', 'n_genes'])
            return self.pathway_coherence

        df = pd.DataFrame(results).sort_values('lambda2_internal', ascending=False)
        self.pathway_coherence = df
        return df

    def plot_coherence(self, output_file='user/pathway_coherence.png', top_n=15):
        if self.pathway_coherence.empty: return
        df = self.pathway_coherence.head(top_n).copy().iloc[::-1]
        plt.figure(figsize=(10, 8))
        colors = ['#27ae60' if x > 0.5 else '#f39c12' if x > 0.3 else '#e74c3c' for x in df['lambda2_internal']]
        plt.barh(df['pathway'], df['lambda2_internal'], color=colors, edgecolor='black')
        plt.axvline(x=0.5, color='green', linestyle='--', alpha=0.5)
        plt.xlabel('Internal Phase Coherence (λ₂)')
        plt.title('Top Pathways by Phase Stability')
        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        plt.close()

class SingleCellEqtlMapper:
    """Mapeia SNPs para genes usando dados eQTL (Bulk ou Single-Cell)."""
    def __init__(self):
        self.mapping = {}

    def load_eqtl(self, filepath: str):
        """Loads eQTL data: SNP, GENE, (optional) CELL_TYPE."""
        df = pd.read_csv(filepath, sep='\t')
        df.columns = [c.upper() for c in df.columns]
        # Store as Dict {SNP: [GENES]}
        self.mapping = df.groupby('SNP')['GENE'].apply(list).to_dict()
        return self.mapping

    def simulate_mapping(self, snps, cell_type='Neuron'):
        # Mock mapping for simulation
        for snp in snps:
            self.mapping[snp] = [f"SC_{cell_type.upper()}_GENE_{snp.replace('rs', '')}"]
        return self.mapping

class CrossDisorderAnalyzer:
    """Analyzes overlap and phase alignment between disorders."""
    def compute_gene_phase_angle(self, gene, snp_to_gene1, snp_to_gene2, df1, df2):
        snps1 = [s for s, g_list in snp_to_gene1.items() if gene in g_list]
        snps2 = [s for s, g_list in snp_to_gene2.items() if gene in g_list]
        common = set(snps1).intersection(set(snps2))
        if not common: return np.nan

        diff_angles = []
        for snp in common:
            t1 = np.arctan2(df1[df1['SNP'] == snp]['BETA'].values[0], 1.0)
            t2 = np.arctan2(df2[df2['SNP'] == snp]['BETA'].values[0], 1.0)
            diff = np.angle(np.exp(1j * t1) * np.conj(np.exp(1j * t2)))
            diff_angles.append(np.degrees(diff))
        return np.mean(diff_angles)

    def plot_venn_with_phase(self, set1, set2, gene_phase_angles, title="Overlap", output="user/venn_phase.png"):
        plt.figure(figsize=(8, 8))
        v = venn2([set1, set2], set_labels=('Disorder A', 'Disorder B'))
        if len(gene_phase_angles) > 0:
            avg_angle = np.nanmean(list(gene_phase_angles.values()))
            norm_angle = np.abs(avg_angle) / 180.0
            cmap = plt.cm.RdYlGn_r
            color = cmap(norm_angle)
            if v.get_patch_by_id('11'):
                v.get_patch_by_id('11').set_color(color)
                v.get_patch_by_id('11').set_alpha(0.7)
        plt.title(title)
        plt.savefig(output, dpi=150)
        plt.close()

class ArkhePGC:
    def __init__(self, window_size_bp=250000):
        self.window_size = window_size_bp

    def calculate_metrics(self, df):
        df['weight'] = 1.0 / (df['SE'] ** 2 + 1e-10)
        df['phase'] = np.arctan2(df['BETA'], 1.0)
        df['complex_vec'] = np.exp(1j * df['phase'])
        return df

    def ld_clumping(self, df):
        if df.empty: return df
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

def simulate_realistic_gwas(n_snps=10000, seed=42):
    """
    Generates GWAS data where λ₂ reduction and enrichment are observable.
    """
    np.random.seed(seed)
    positions = np.sort(np.random.uniform(0, 100e6, n_snps))

    # Background noise
    beta = np.random.normal(0, 0.1, n_snps)
    se = np.abs(np.random.normal(0.2, 0.05, n_snps)) + 0.05

    # Causal blocks (LD)
    n_causal_loci = 25
    causal_idx = np.random.choice(n_snps, n_causal_loci, replace=False)

    for i in causal_idx:
        # High effect for causal SNP
        effect = np.random.choice([-1, 1]) * np.random.uniform(0.5, 1.0)
        # LD Window
        nearby = (positions >= positions[i] - 200000) & (positions <= positions[i] + 200000)
        beta[nearby] = effect + np.random.normal(0, 0.05, np.sum(nearby))
        se[nearby] = np.random.uniform(0.02, 0.05, np.sum(nearby))

    z = beta / se
    p = 2 * norm.sf(np.abs(z))

    df = pd.DataFrame({
        'SNP': [f'rs{i}' for i in range(n_snps)],
        'CHR': 1,
        'BP': positions.astype(int),
        'BETA': beta,
        'SE': se,
        'P': p
    })
    return df
