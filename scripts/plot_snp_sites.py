#!/usr/bin/env python
# author: enzedeng
import os
import argparse
import pysam
from matplotlib import pyplot as plt
from matplotlib_venn import venn3_unweighted

def load_vcf(vcf_fn):
    snp_set = set()
    with pysam.VariantFile(vcf_fn) as f:
        for record in f.fetch():
            # print(record.chrom, record.pos, record.ref, record.alts)
            # only snp
            snp_set.add((record.chrom, record.pos - 1, record.ref, record.alts[0]))
    return snp_set

def main():
    parser = argparse.ArgumentParser(description='Extract SNP from different sample.')
    parser.add_argument('--outpre', required=True, help = 'Output prefix of data.')
    parser.add_argument('--mixed_vcf', required=True, help = 'vcf file of mixed library.')
    parser.add_argument('vcfs', nargs=2, help = 'vcf file with passed SNP.')
    args = parser.parse_args()

    snp_vcf1, snp_vcf2 = args.vcfs
    sample1 = os.path.basename(snp_vcf1).split('.')[0]
    sample2 = os.path.basename(snp_vcf2).split('.')[0]
    sample1_vcf = load_vcf(snp_vcf1)
    sample2_vcf = load_vcf(snp_vcf2)
    mixed_vcf = load_vcf(args.mixed_vcf)
    snps = {sample1: sample1_vcf,
            sample2: sample2_vcf,
            'mixed': mixed_vcf}

    venn3_unweighted(snps.values(), snps.keys(), set_colors=('#FF6666','#66FF66','#6666FF'), alpha=1)
    plt.title(f"Number of SNPs detected")
    plt.savefig(f'{args.outpre}venn_snp.png', dpi=600, bbox_inches='tight')

if __name__ == '__main__':
    main()
