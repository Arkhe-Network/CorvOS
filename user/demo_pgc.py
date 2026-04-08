#!/usr/bin/env python3
"""
Demo for Arkhe-PGC v4.2: Functional Phase Genetics.
"""

from arkhe_pgc import ArkhePGC, simulate_realistic_gwas, PathwayCoherenceAnalyzer, SingleCellEqtlMapper
import pandas as pd
import numpy as np

def run_pgc_demo():
    print("🧬 Arkhe-PGC v4.2: Functional Phase Genetics Demo")
    print("="*60)

    # 1. Simulate GWAS
    df = simulate_realistic_gwas(n_snps=2000)
    pgc = ArkhePGC()
    df = pgc.calculate_metrics(df)

    # 2. Simulate eQTL Mapping
    mapper = SingleCellEqtlMapper()
    snps = df['SNP'].tolist()
    snp_to_genes = mapper.simulate_mapping(snps, cell_type='Neuron')

    # 3. Define Pathways
    pathways = {
        "Synaptic_Transmission": set([f"SC_NEURON_GENE_{i}" for i in range(100)]),
        "Glutamate_Receptor_Activity": set([f"SC_NEURON_GENE_{i}" for i in range(50, 150)]),
        "Dopamine_Metabolism": set([f"SC_NEURON_GENE_{i}" for i in range(500, 600)])
    }

    # 4. Pathway Analysis
    pca = PathwayCoherenceAnalyzer(pathways)

    print("\n[*] Calculating Pathway Coherence (λ₂)...")
    df_coh = pca.calculate_pathway_coherence(df, snp_to_genes)
    print(df_coh[['pathway', 'lambda2_internal', 'n_snps']])

    print("\n[*] Calculating Pathway Enrichment (Hypergeometric)...")
    df_enrich = pca.compute_pathway_enrichment(df, snp_to_genes, p_threshold=0.01)
    print(df_enrich[['pathway', 'p_value', 'overlap', 'fold_enrichment']])

    # 5. Global Coherence
    df_pruned = pgc.ld_clumping(df)
    global_lambda = pgc.compute_coherence(df_pruned)
    print(f"\n[SUMMARY] Global λ₂ (Clumped): {global_lambda:.4f}")

    print("\n" + "="*60)
    print("Arkhe-PGC Demo Complete.")

if __name__ == "__main__":
    run_pgc_demo()
