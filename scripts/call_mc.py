#!/usr/local/apps/python/2.7.8/bin/python
import sys
import getopt
from methylpy.call_mc import call_methylated_sites

def main(argv):
	input_file=argv[0]
	sample_name=argv[1]
	ref_genome=argv[2]
	ref_chr=argv[3]+":"
	num_procs=argv[4]
	sort_mem=argv[5]+"G"


	call_methylated_sites(input_file, #bam file
                      	sample_name, #sample name
                      	ref_genome, #reference genome (fasta)
                      	ref_chr,
						"1.8",
						num_procs=num_procs,
						min_cov=3,
						binom_test=True,
						sort_mem=sort_mem,
						bh=True,
						sig_cutoff=0.01)

if __name__ == "__main__":
   main(sys.argv[1:])
