import os
import sys

functionsfile = '../../../scripts/functions.py'
sys.path.append(os.path.dirname(os.path.expanduser(functionsfile)))

import functions

allc=sys.argv[1]+"_allc_total.tsv"
genome_file="../ref/"+sys.argv[1]+".genome"
features="../ref/"+sys.argv[1]+".gff"
filter_chr=['ChrL','ChrC','ChrM']
context=['CG','CHG','CHH','CAA','CAT','CAC','CAG','CTA','CTT','CTC',
         'CTG','CCA','CCT','CCC','CCG','CGA','CGT','CGC','CGG']

if os.path.exists(features):
    print("Gene metaplot")
#    functions.map2features(allc,features,genome_file,updown_stream=0,
#                           first_feature='gene',second_feature='exon',filter_chr=filter_chr)
    functions.feature_mC_levels('CDS_allc.tmp',features,output="results/gene_methylation_levels.tsv",
                                cutoff=0,filter_features='gene',filter_chr=filter_chr)

else:
    print("No gene annotations found")

#os.remove('CDS_allc.tmp')
os.remove('f_tmp')
os.remove('c_tmp')
