#!/usr/bin/env python3
"""
Arkhe-PGC v3.0: Genetic Phase Coherence & Pathway Enrichment Analysis.
Integrated module for LD clumping, IVW coherence, and biological function mapping.
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import time
import os
import warnings

warnings.filterwarnings('ignore')

class ArkhePGC:
    def __init__(self, window_size_bp=250000):
        self.window_size = window_size_bp
        self.snp_to_genes = {}
        self.pathway_genes = {}

    # --- PHASE & COHERENCE ---

    def calculate_metrics(self, df, use_ivw=True):
        """
        Calculates weights and complex phases using quadrant-aware mapping.
        """
        if use_ivw and 'SE' in df.columns:
            df['weight'] = 1.0 / (df['SE'] ** 2 + 1e-10)
        else:
            df['weight'] = -np.log10(np.clip(df['P'], 1e-300, 1))

        # Scaling for robust phase calculation
        b_val = df['BETA'].values
        w_val = df['weight'].values
        b_scale = np.std(b_val) if np.std(b_val) > 0 else 1.0
        w_scale = np.std(w_val) if np.std(w_val) > 0 else 1.0

        df['theta'] = np.angle((b_val / b_scale) + 1j * (w_val / w_scale))
        df['complex_vec'] = np.exp(1j * df['theta'])
        return df

    def compute_coherence(self, df):
        """Weighted Kuramoto Parameter λ₂."""
        if df.empty: return 0.0
        w = df['weight'].values
        z = df['complex_vec'].values
        return np.abs(np.sum(w * z)) / np.sum(w)

    # --- LD PRUNING (CLUMPING) ---

    def ld_clumping(self, df):
        """Physical Clumping to reduce LD inflation."""
        if df.empty: return df
        df = df.sort_values(by=['CHR', 'weight'], ascending=[True, False])
        pruned_list = []
        for chrom in df['CHR'].unique():
            chrom_df = df[df['CHR'] == chrom].copy()
            while not chrom_df.empty:
                lead_snp = chrom_df.iloc[0]
                pruned_list.append(lead_snp)
                mask = (chrom_df['BP'] >= lead_snp['BP'] - self.window_size) & \
                       (chrom_df['BP'] <= lead_snp['BP'] + self.window_size)
                chrom_df = chrom_df[~mask]
        return pd.DataFrame(pruned_list)

    # --- PATHWAY ENRICHMENT ---

    def fetch_online_annotations(self, snps, batch_size=200):
        """Fetches Ensembl annotations (simulated/mocked for demo)."""
        # In a real scenario, this would call Ensembl REST API.
        # For the demonstration, we'll map SNPs to mock gene IDs.
        for snp in snps:
            self.snp_to_genes[snp] = f"GENE_{snp.replace('rs', '')}"
        return self.snp_to_genes

    def load_gene_sets(self, mock=True):
        """Loads GMT gene sets (mocked for demo)."""
        if mock:
            self.pathway_genes = {
                "Calcium_Signaling": {f"GENE_{i}" for i in range(100)},
                "Glutamatergic_Synapse": {f"GENE_{i}" for i in range(50, 150)},
                "Dopaminergic_Synapse": {f"GENE_{i}" for i in range(150, 250)},
                "Neuroactive_Ligand_Receptor": {f"GENE_{i}" for i in range(250, 400)}
            }
        return self.pathway_genes

    def analyze_enrichment(self, df_pruned, min_size=5, max_size=500):
        """Hypergeometric test for pathway over-representation."""
        # 1. Map SNPs to Genes
        snp_genes = []
        for snp in df_pruned['SNP']:
            if snp in self.snp_to_genes:
                snp_genes.append(self.snp_to_genes[snp])

        gene_set = set(snp_genes)
        if not gene_set: return pd.DataFrame()

        # 2. Background: all genes in any pathway
        background_genes = set()
        for genes in self.pathway_genes.values():
            background_genes.update(genes)

        results = []
        N = len(background_genes)
        n = len(gene_set.intersection(background_genes))

        for pathway, p_genes in self.pathway_genes.items():
            if len(p_genes) < min_size or len(p_genes) > max_size: continue

            overlap = gene_set.intersection(p_genes)
            k = len(overlap)
            K = len(p_genes.intersection(background_genes))

            if k > 0:
                p_val = stats.hypergeom.sf(k - 1, N, K, n)
                enrichment = (k/n) / (K/N) if K > 0 else 0
                results.append({
                    'Pathway': pathway,
                    'Hits': k,
                    'Pathway_Size': K,
                    'Enrichment': enrichment,
                    'P-value': p_val
                })

        res_df = pd.DataFrame(results)
        if not res_df.empty:
            res_df['FDR_adj_P'] = self.apply_fdr(res_df['P-value'].values)
            return res_df.sort_values('P-value')
        return res_df

    def apply_fdr(self, p_values):
        """Benjamini-Hochberg FDR correction."""
        m = len(p_values)
        sorted_indices = np.argsort(p_values)
        sorted_p = p_values[sorted_indices]
        fdr = np.zeros(m)
        prev_fdr = 1.0
        for i in range(m - 1, -1, -1):
            rank = i + 1
            current_fdr = (sorted_p[i] * m) / rank
            current_fdr = min(current_fdr, prev_fdr)
            fdr[i] = current_fdr
            prev_fdr = current_fdr
        final_fdr = np.zeros(m)
        final_fdr[sorted_indices] = fdr
        return final_fdr

    def visualize_enrichment(self, df, output_file='enrichment_plot.png'):
        """Bubble plot for enrichment results."""
        if df.empty: return
        df_plot = df.head(15)
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df_plot, x='Enrichment', y='Pathway',
                        size='Hits', hue='FDR_adj_P',
                        palette='viridis_r', sizes=(40, 400), alpha=0.7)
        plt.title('Arkhe-PGC v3.0: Pathway Enrichment Analysis')
        plt.tight_layout()
        plt.savefig(output_file, dpi=150)
        plt.close()

# --- REALISTIC SIMULATION ---

def simulate_realistic_gwas(n_snps=10000, seed=42):
    np.random.seed(seed)
    positions = np.sort(np.random.uniform(0, 100e6, n_snps))
    beta = np.random.normal(0, 0.05, n_snps)
    se = np.abs(np.random.normal(0.1, 0.02, n_snps)) + 0.05

    # Causal signals at specific "pathway" indices
    # We'll make SNPs rs0 to rs100 belong to "Calcium_Signaling"
    causal_indices = list(range(0, 100)) + list(range(1000, 1100))
    for i in causal_indices:
        beta[i] = np.random.choice([-1, 1]) * np.random.uniform(0.5, 0.8)
        se[i] = np.random.uniform(0.01, 0.04)

    z = beta / se
    p = 2 * stats.norm.sf(np.abs(z))
    return pd.DataFrame({
        'SNP': [f'rs{i}' for i in range(n_snps)],
        'CHR': 1,
        'BP': positions.astype(int),
        'BETA': beta,
        'SE': se,
        'P': p
    })
