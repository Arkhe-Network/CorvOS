#!/usr/bin/env python3
from arkhe_pgc import ArkhePGC, PathwayCoherenceAnalyzer, SingleCellEqtlMapper, CrossDisorderAnalyzer
import pandas as pd
import numpy as np
import os

def run_pipeline():
    print("🚀 Running Arkhe-PGC v4.1 Integrated Pipeline...")
    os.makedirs('user', exist_ok=True)

    # 1. Load Data
    scz_gwas = pd.read_csv('user/data/scz_gwas.tsv', sep='\t')
    bip_gwas = pd.read_csv('user/data/bip_gwas.tsv', sep='\t')

    # 2. Genetics Engine
    pgc = ArkhePGC()
    scz_gwas = pgc.calculate_metrics(scz_gwas)
    bip_gwas = pgc.calculate_metrics(bip_gwas)

    scz_pruned = pgc.ld_clumping(scz_gwas)
    bip_pruned = pgc.ld_clumping(bip_gwas)

    # 3. Functional Mapping
    mapper = SingleCellEqtlMapper()
    snp_to_gene = mapper.load_eqtl('user/data/brain_sceqtl.tsv')

    # 4. Pathway Coherence
    pathway_db = {
        'Neuronal_Synapse': {f'GENE_{i}' for i in range(50)},
        'Calcium_Channel': {f'GENE_{i}' for i in range(50, 100)}
    }
    pca = PathwayCoherenceAnalyzer(pathway_db)
    path_report = pca.calculate_pathway_coherence(scz_pruned, snp_to_gene, min_snps=1)
    print("\nPathway Coherence Report (SCZ):")
    print(path_report)
    pca.plot_coherence(output_file='user/pathway_coherence.png')

    # 5. Cross-Disorder Venn
    cda = CrossDisorderAnalyzer()
    genes_scz = set().union(*[snp_to_gene[s] for s in scz_pruned['SNP'] if s in snp_to_gene])
    genes_bip = set().union(*[snp_to_gene[s] for s in bip_pruned['SNP'] if s in snp_to_gene])

    shared_genes = genes_scz.intersection(genes_bip)
    gene_angles = {}
    for gene in shared_genes:
        angle = cda.compute_gene_phase_angle(gene, snp_to_gene, snp_to_gene, scz_gwas, bip_gwas)
        gene_angles[gene] = angle

    cda.plot_venn_with_phase(genes_scz, genes_bip, gene_angles, title="SCZ vs BIP Overlap", output='user/venn_phase.png')

    print("\n✅ Pipeline execution complete. Visualizations saved in user/")

if __name__ == "__main__":
    run_pipeline()
