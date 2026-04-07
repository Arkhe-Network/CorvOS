#!/usr/bin/env python3
"""
Demonstration of Arkhe-PGC v3.0 Pipeline:
Simulation -> LD Clumping -> Coherence -> Enrichment Analysis
"""

from arkhe_pgc import ArkhePGC, simulate_realistic_gwas
import numpy as np

def run_demo():
    print("🧬 Arkhe-PGC v3.0: Genetic Coherence & Pathway Enrichment Demo")
    print("="*60)

    # 1. Simulate Realistic GWAS Data
    n_snps = 5000
    df = simulate_realistic_gwas(n_snps=n_snps, seed=42)
    print(f"Simulated GWAS with {n_snps} SNPs.")

    processor = ArkhePGC(window_size_bp=250000)

    # 2. Step 1: Initial Metrics & Raw Coherence
    df = processor.calculate_metrics(df)
    lambda_raw = processor.compute_coherence(df)
    print(f"\nInitial λ₂ (with LD inflation): {lambda_raw:.4f}")

    # 3. Step 2: LD Clumping (Pruning)
    df_pruned = processor.ld_clumping(df)
    print(f"Retained {len(df_pruned)} SNPs after physical clumping.")

    # 4. Step 3: Pruned Coherence
    lambda_pruned = processor.compute_coherence(df_pruned)
    print(f"Pruned λ₂ (Real biological signal): {lambda_pruned:.4f}")

    reduction = (1 - lambda_pruned / lambda_raw) * 100
    print(f"Reduction in Coherence Inflation: {reduction:.1f}%")

    # 5. Step 4: Pathway Enrichment
    print("\nRunning Pathway Enrichment...")
    processor.fetch_online_annotations(df_pruned['SNP'].tolist())
    processor.load_gene_sets(mock=True)

    enrichment = processor.analyze_enrichment(df_pruned)

    if not enrichment.empty:
        print("\nTop Enriched Pathways (FDR Corrected):")
        print(enrichment[['Pathway', 'Hits', 'Enrichment', 'FDR_adj_P']].head())

        # Save visualization
        processor.visualize_enrichment(enrichment, output_file='user/arkhe_enrichment.png')
        print(f"\n📊 Enrichment plot saved to user/arkhe_enrichment.png")
    else:
        print("\nNo significant enrichment found.")

    print("\n" + "="*60)
    print("Conclusion: Arkhe-PGC successfully identifies independent biological signals")
    print("and maps them to functional pathways using hypergeometric testing and FDR.")

if __name__ == "__main__":
    run_demo()
