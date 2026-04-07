#!/usr/bin/env python3
"""
Arkhe-PGC v4.0: Functional & Cross-Disorder Phase Genetics Framework.
Integrated with GTEx/Single-Cell mapping, Cross-Disorder overlap, and Quadrant Phase Analysis.
"""

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')

class ArkhePGC:
    def __init__(self, window_size_bp=250000):
        self.window_size = window_size_bp
        self.snp_to_genes = {}
        self.pathway_genes = {}
        self.cell_type_eqtl_map = {}

    # --- CORE PHASE & COHERENCE ---

    def calculate_metrics(self, df, use_ivw=True):
        """Calculates weights and complex phases using quadrant-aware mapping."""
        if use_ivw and 'SE' in df.columns:
            df['weight'] = 1.0 / (df['SE'] ** 2 + 1e-10)
        else:
            df['weight'] = -np.log10(np.clip(df['P'], 1e-300, 1))

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

    # --- ADVANCED MAPPING (GTEx & Single-Cell) ---

    def map_functional_genes(self, df, method='gtex_brain'):
        """
        Maps SNPs to genes using eQTL signals.
        'gtex_brain': Standard brain tissue eQTLs.
        'single_cell': Cell-type specific eQTLs (Neuronal, Glial).
        """
        mapping = {}
        for snp in df['SNP']:
            if method == 'single_cell':
                # Mock Single-Cell mapping: SNPs rs0-rs49 are Neuronal, rs50-rs99 are Glial
                snp_id = int(snp.replace('rs', ''))
                if snp_id < 50:
                    mapping[snp] = {'gene': f"NEURON_GENE_{snp_id}", 'cell': 'Excitatory_Neuron'}
                else:
                    mapping[snp] = {'gene': f"GLIA_GENE_{snp_id}", 'cell': 'Microglia'}
            else:
                # Mock GTEx Brain mapping
                mapping[snp] = {'gene': f"REG_GENE_{snp.replace('rs', '')}", 'cell': 'Whole_Brain'}

        self.snp_to_genes = mapping
        return mapping

    # --- CROSS-DISORDER ANALYSIS ---

    def cross_disorder_coherence(self, df1, df2):
        """
        Calculates λ_AB: cross-disorder phase alignment.
        """
        common = pd.merge(df1, df2, on='SNP', suffixes=('_A', '_B'))
        if common.empty: return 0.0

        w_a = common['weight_A'].values
        w_b = common['weight_B'].values
        c_a = common['complex_vec_A'].values
        c_b = common['complex_vec_B'].values

        combined_w = w_a * w_b
        phase_diff = c_a * np.conj(c_b)

        lambda_ab = np.abs(np.sum(combined_w * phase_diff)) / np.sum(combined_w)
        return lambda_ab

    # --- PATHWAY ENRICHMENT ---

    def analyze_enrichment(self, df_pruned, pathway_map):
        """Hypergeometric enrichment with internal pathway coherence score."""
        gene_set = {v['gene'] for k, v in self.snp_to_genes.items() if k in set(df_pruned['SNP'])}

        all_pathway_genes = set()
        for genes in pathway_map.values():
            all_pathway_genes.update(genes)

        results = []
        N = len(all_pathway_genes)
        n = len(gene_set.intersection(all_pathway_genes))

        for name, p_genes in pathway_map.items():
            overlap = gene_set.intersection(p_genes)
            k = len(overlap)
            K = len(set(p_genes).intersection(all_pathway_genes))

            if k > 0:
                p_val = stats.hypergeom.sf(k - 1, N, K, n)
                # Internal phase stability for this pathway
                p_coherence = self._compute_internal_pathway_coherence(df_pruned, overlap)
                results.append({
                    'Pathway': name,
                    'Hits': k,
                    'Enrichment': (k/n) / (K/N) if K > 0 else 0,
                    'P-value': p_val,
                    'Path_Coherence': p_coherence
                })

        res_df = pd.DataFrame(results).sort_values('P-value')
        return res_df

    def _compute_internal_pathway_coherence(self, df, genes_in_pathway):
        """Calculates λ₂ specifically for SNPs contributing to a pathway."""
        relevant_snps = [k for k, v in self.snp_to_genes.items() if v['gene'] in genes_in_pathway]
        path_df = df[df['SNP'].isin(relevant_snps)]
        return self.compute_coherence(path_df)

    # --- VISUALIZATION ---

    def plot_phase_overlap_quadrant(self, df1, df2, output_file='user/phase_quadrant.png'):
        """Polar plot showing phase alignment between two disorders."""
        common = pd.merge(df1, df2, on='SNP', suffixes=('_A', '_B'))
        if common.empty: return

        # Calculate angular difference
        delta_theta = common['theta_A'] - common['theta_B']
        weights = common['weight_A'] * common['weight_B']

        plt.figure(figsize=(8, 8))
        ax = plt.subplot(111, projection='polar')

        # Scatter plot of phase differences
        ax.scatter(delta_theta, weights, alpha=0.5, c=delta_theta, cmap='hsv', s=20)
        ax.set_title("Cross-Disorder Phase Overlap (Δθ)", va='bottom')
        plt.savefig(output_file, dpi=150)
        plt.close()

    def plot_venn_shared_genes(self, df1_pruned, df2_pruned, output_file='user/gene_venn.png'):
        """Plots simulated Venn overlap of mapped genes."""
        g1 = {v['gene'] for k, v in self.map_functional_genes(df1_pruned).items()}
        g2 = {v['gene'] for k, v in self.map_functional_genes(df2_pruned).items()}

        only_1 = len(g1 - g2)
        only_2 = len(g2 - g1)
        shared = len(g1 & g2)

        plt.figure(figsize=(8, 5))
        plt.bar(['Disorder A', 'Shared', 'Disorder B'], [only_1, shared, only_2], color=['blue', 'purple', 'red'])
        plt.title("Functional Gene Overlap (eQTL Mapped)")
        plt.ylabel("Number of Unique Genes")
        plt.savefig(output_file, dpi=150)
        plt.close()

# --- ADVANCED SIMULATION ---

def simulate_gwas_pair(n_snps=10000, overlap_fraction=0.3, seed=42):
    """Simulates two GWAS datasets with a shared genetic architecture."""
    np.random.seed(seed)
    positions = np.sort(np.random.uniform(0, 100e6, n_snps))
    snps = [f'rs{i}' for i in range(n_snps)]

    def generate_df(is_shared):
        beta = np.random.normal(0, 0.05, n_snps)
        se = np.abs(np.random.normal(0.1, 0.02, n_snps)) + 0.05
        # Add shared causal signals
        shared_indices = np.random.choice(n_snps, int(n_snps * 0.05), replace=False)
        for i in shared_indices:
            beta[i] = np.random.uniform(0.4, 0.7)
            se[i] = 0.02
        z = beta / se
        p = 2 * stats.norm.sf(np.abs(z))
        return pd.DataFrame({'SNP': snps, 'CHR': 1, 'BP': positions.astype(int), 'BETA': beta, 'SE': se, 'P': p})

    return generate_df(True), generate_df(True)
