#!/usr/bin/env python3
"""
Comprehensive Demonstration of Arkhe-PGC v4.0:
Cross-Disorder Phase Architecture, Single-Cell eQTLs, and Quadrant Analysis.
"""

from arkhe_pgc import ArkhePGC, simulate_gwas_pair
import numpy as np
import os

def run_v4_demo():
    print("🧬 Arkhe-PGC v4.0: Comprehensive Transdiagnostic Demo")
    print("="*60)

    # 1. Simulate SCZ and BIP datasets
    n_snps = 5000
    df_scz, df_bip = simulate_gwas_pair(n_snps=n_snps, overlap_fraction=0.5, seed=42)
    print(f"Simulated SCZ and BIP datasets ({n_snps} SNPs each).")

    processor = ArkhePGC(window_size_bp=250000)

    # 2. Process metrics
    df_scz = processor.calculate_metrics(df_scz)
    df_bip = processor.calculate_metrics(df_bip)

    scz_pruned = processor.ld_clumping(df_scz)
    bip_pruned = processor.ld_clumping(df_bip)

    print(f"SCZ λ₂: {processor.compute_coherence(scz_pruned):.4f}")
    print(f"BIP λ₂: {processor.compute_coherence(bip_pruned):.4f}")

    # 3. Cross-Disorder Phase Alignment
    lambda_ab = processor.cross_disorder_coherence(scz_pruned, bip_pruned)
    print(f"\nCross-Disorder Coherence λ_AB: {lambda_ab:.4f}")

    # 4. Advanced Mapping: Single-Cell Resolution
    print("\nFunctional Mapping (Cell-Type Resolution):")
    processor.map_functional_genes(scz_pruned, method='single_cell')

    # Pathway analysis for Neuronal Sync
    pathway_map = {
        'Neuronal_Sync': [f"NEURON_GENE_{i}" for i in range(50)],
        'Glial_Metabolism': [f"GLIA_GENE_{i}" for i in range(50, 100)]
    }

    enrichment = processor.analyze_enrichment(scz_pruned, pathway_map)
    print("\nEnrichment & Internal Pathway Coherence (SCZ):")
    print(enrichment[['Pathway', 'Enrichment', 'Path_Coherence', 'P-value']])

    # 5. Advanced Visualizations
    print("\nGenerating Advanced Visualizations...")
    os.makedirs('user', exist_ok=True)
    processor.plot_phase_overlap_quadrant(scz_pruned, bip_pruned, output_file='user/arkhe_phase_polar.png')
    processor.plot_venn_shared_genes(scz_pruned, bip_pruned, output_file='user/arkhe_gene_overlap.png')

    print("📊 Polar Phase Plot saved to user/arkhe_phase_polar.png")
    print("📊 Gene Overlap Plot saved to user/arkhe_gene_overlap.png")

    print("\n" + "="*60)
    print("Conclusion: Arkhe-PGC v4.0 provides a complete transdiagnostic view,")
    print("mapping shared phase architectures across disorders with functional precision.")

if __name__ == "__main__":
    run_v4_demo()
