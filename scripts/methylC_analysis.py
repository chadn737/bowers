import os
import sys
import pandas as pd
import pybedtools as pbt

functionsfile = '../../../scripts/functions.py'
sys.path.append(os.path.dirname(os.path.expanduser(functionsfile)))

import functions

allc=sys.argv[1]+"_allc_total.tsv"
fasta="../ref/methylCseq/"+sys.argv[1]+"_"+sys.argv[2]+".fa"
genome_file="../ref/"+sys.argv[1]+".genome"
features="../ref/"+sys.argv[1]+".gff"
filter_chr=['ChrL','ChrC','ChrM']
context=['CG','CHG','CHH','CAA','CAT','CAC','CAG','CTA','CTT','CTC',
         'CTG','CCA','CCT','CCC','CCG','CGA','CGT','CGC','CGG']

if os.path.exists(feayures):
    print("Gene metaplot")
    functions.map2features(allc,features,genome_file,updown_stream=0,
                           first_feature='gene',second_feature='exon',filter_chr=filter_chr)
    functions.feature_mC_levels('CDS_allc.tmp',features,output="results/gene_methylation_levels.tsv",
                                cutoff=0,filter_features='gene',filter_chr=filter_chr)
#    functions.gene_binom_test("results/gene_methylation_levels.tsv",output="results/gene_methylation_levels.tsv")

else:
    print("No gene annotations found")

#os.remove('CDS_allc.tmp')
