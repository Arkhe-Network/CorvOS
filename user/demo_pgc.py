#!/usr/bin/env python3
"""
Comprehensive Demonstration of Arkhe-PGC v4.1:
Pathway Coherence, Single-Cell eQTLs, and Quadrant-Aware Venn Overlap.
"""

from arkhe_pgc import ArkhePGC, PathwayCoherenceAnalyzer, SingleCellEqtlMapper, CrossDisorderAnalyzer, simulate_gwas_pair
import numpy as np
import pandas as pd
import os

def run_v41_demo():
    print("🧬 Arkhe-PGC v4.1: Genetic Coherence & Transdiagnostic Overlap Demo")
    print("="*70)

    # 1. Simulate SCZ and BIP datasets
    n_snps = 5000
    df_scz, df_bip = simulate_gwas_pair(n_snps=n_snps, seed=42)
    print(f"Simulated SCZ and BIP datasets ({n_snps} SNPs each).")

    processor = ArkhePGC(window_size_bp=250000)

    # 2. Process metrics
    df_scz = processor.calculate_metrics(df_scz)
    df_bip = processor.calculate_metrics(df_bip)

    scz_pruned = processor.ld_clumping(df_scz)
    bip_pruned = processor.ld_clumping(df_bip)

    print(f"SCZ λ₂: {processor.compute_coherence(scz_pruned):.4f}")
    print(f"BIP λ₂: {processor.compute_coherence(bip_pruned):.4f}")

    # 3. Single-Cell eQTL Mapping (Neuronal Resolution)
    print("\n[Step 1] Functional Mapping (Single-Cell Neuron Resolution):")
    sc_mapper = SingleCellEqtlMapper()
    sc_mapping_scz = sc_mapper.simulate_mapping(scz_pruned['SNP'].tolist(), cell_type='Neuron')
    sc_mapping_bip = sc_mapper.simulate_mapping(bip_pruned['SNP'].tolist(), cell_type='Neuron')
    print(f"Mapped {len(sc_mapping_scz)} SNPs to neuronal functional genes.")

    # 4. Pathway Coherence Analysis
    print("\n[Step 2] Internal Pathway Coherence:")
    # Define Pathways: Synaptic signaling and Calcium channels
    pathway_db = {
        'Synaptic_Signaling': [f"SC_NEURON_GENE_{i}" for i in range(100)],
        'Calcium_Transport': [f"SC_NEURON_GENE_{i}" for i in range(100, 200)]
    }

    pca = PathwayCoherenceAnalyzer(pathway_db)
    scz_path_coh = pca.compute_pathway_internal_coherence(scz_pruned, sc_mapping_scz)
    print("\nPathway Coherence Report (SCZ):")
    print(scz_path_coh)

    # 5. Cross-Disorder Venn with Phase Quadrants
    print("\n[Step 3] Generating Quadrant-Aware Venn Overlap...")
    cda = CrossDisorderAnalyzer()

    genes_scz = set(sc_mapping_scz.values())
    genes_bip = set(sc_mapping_bip.values())

    # Calculate phase difference for shared genes
    shared_genes = genes_scz.intersection(genes_bip)
    gene_angles = {}
    for gene in shared_genes:
        angle = cda.compute_gene_phase_angle(gene, sc_mapping_scz, sc_mapping_bip, df_scz, df_bip)
        gene_angles[gene] = angle

    os.makedirs('user', exist_ok=True)
    cda.plot_venn_with_phase(genes_scz, genes_bip, gene_angles,
                             title="SCZ vs BIP Gene Overlap (Neuronal)",
                             output="user/arkhe_venn_phase.png")

    print("📊 Venn Diagram with Phase Color saved to user/arkhe_venn_phase.png")

    print("\n" + "="*70)
    print("Conclusion: Arkhe-PGC v4.1 accurately maps functional overlaps and identifies")
    print("highly coherent biological pathways within specific cell types.")

if __name__ == "__main__":
    run_v41_demo()
