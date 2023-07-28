#!/usr/bin/env python
# author: enzedeng
import os
import argparse
import pysam

def load_vcf(vcf_fn):
    snp_dict = dict()
    with pysam.VariantFile(vcf_fn) as f:
        for record in f.fetch():
            # print(record.chrom, record.pos, record.ref, record.alts)
            # only snp
            snp_dict[(record.chrom, record.pos - 1)] = (record.ref, record.alts[0])
    return snp_dict

def write_vcf(vcf_fn, snps, out_fn):
    with pysam.VariantFile(vcf_fn) as f, pysam.VariantFile(out_fn, 'w', header=f.header) as o:
        for record in f.fetch():
            if (record.chrom, record.pos -1 ) not in snps:
                continue
            o.write(record)
            # only snp

def main():
    parser = argparse.ArgumentParser(description='Extract SNP from different sample.')
    parser.add_argument('--outpre', required=True, help = 'Output prefix of data.')
    parser.add_argument('vcfs', nargs=2, help = 'vcf file with passed SNP.')
    args = parser.parse_args()

    snp_vcf1, snp_vcf2 = args.vcfs
    sample1 = os.path.basename(snp_vcf1).split('.')[0]
    sample2 = os.path.basename(snp_vcf2).split('.')[0]
    sample1_vcf = load_vcf(snp_vcf1)
    sample2_vcf = load_vcf(snp_vcf2)
    # enough for classify cells
    only_sample1 = set(x for x in sample1_vcf if x not in sample2_vcf)
    only_sample2 = set(x for x in sample2_vcf if x not in sample1_vcf)
    write_vcf(snp_vcf1, only_sample1, f'{args.outpre}{sample1}.vcf')
    write_vcf(snp_vcf2, only_sample2, f'{args.outpre}{sample2}.vcf')

if __name__ == '__main__':
    main()
