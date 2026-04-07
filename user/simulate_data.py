#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os

def generate_synthetic_data():
    np.random.seed(42)
    os.makedirs('user/data', exist_ok=True)

    n_snps = 2000
    snps = [f'rs{i}' for i in range(n_snps)]

    # 1. GWAS SCZ
    scz_df = pd.DataFrame({
        'CHR': 1,
        'BP': np.sort(np.random.randint(1, 10000000, n_snps)),
        'SNP': snps,
        'BETA': np.random.normal(0, 0.2, n_snps),
        'SE': np.random.uniform(0.01, 0.05, n_snps),
        'P': np.random.uniform(0, 1, n_snps)
    })
    # Add some significant causal signal to first 50 SNPs
    scz_df.loc[:50, 'BETA'] = 0.5 + np.random.normal(0, 0.05, 51)
    scz_df.loc[:50, 'P'] = 1e-12
    scz_df.to_csv('user/data/scz_gwas.tsv', sep='\t', index=False)

    # 2. GWAS BIP (Shared signal with SCZ)
    bip_df = scz_df.copy()
    bip_df['BETA'] = scz_df['BETA'] + np.random.normal(0, 0.1, n_snps)
    bip_df.to_csv('user/data/bip_gwas.tsv', sep='\t', index=False)

    # 3. sc-eQTL Brain
    genes = [f'GENE_{i}' for i in range(200)]
    eqtl_data = []
    # Ensure SNPs map to genes in pathways
    for i in range(200):
        snp = snps[i]
        gene = genes[i % 100]
        eqtl_data.append({
            'SNP': snp,
            'GENE': gene,
            'CELL_TYPE': 'Neuron',
            'PVALUE': 1e-8
        })
    pd.DataFrame(eqtl_data).to_csv('user/data/brain_sceqtl.tsv', sep='\t', index=False)

    print("✅ Synthetic GWAS and sc-eQTL files generated in user/data/")

if __name__ == "__main__":
    generate_synthetic_data()
