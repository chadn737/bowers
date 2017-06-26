import os
import sys

functionsfile = '../../../scripts/functions.py'
sys.path.append(os.path.dirname(os.path.expanduser(functionsfile)))

import functions

allc=sys.argv[1]+'_allc_total.tsv'
genome_file='../ref/'+sys.argv[1]+'.genome'
features='../ref/'+sys.argv[1]+'.gff'
filter_chr=['ChrL','ChrC','ChrM','lcl|Pt','lcl|Mt']
context=['CG','CHG','CHH','CAA','CAT','CAC','CAG','CTA','CTT','CTC',
         'CTG','CCA','CCT','CCC','CCG','CGA','CGT','CGC','CGG']

if os.path.exists(features):
    print('First 150 bps gene methylation')
    functions.get_first_bps(features,genome_file,output='../ref/first_150.gff',
                            first_feature='mRNA',second_feature='CDS',up=150,
                            down=0)
    functions.map2features(allc,'../ref/first_150.gff',genome_file,updown_stream=0,
                          first_feature='CDS',second_feature='CDS',filter_chr=filter_chr)
    functions.feature_mC_levels('CDS_allc.tmp',features,
                                output='results/first_150_methylation_levels.tsv',
                                cutoff=0,filter_features='gene',filter_chr=filter_chr)
    os.remove('CDS_allc.tmp')
    os.remove('f_tmp')
    os.remove('c_tmp')

    print('Gene methylation')
    functions.map2features(allc,features,genome_file,updown_stream=0,
                          first_feature='gene',second_feature='CDS',filter_chr=filter_chr)
    functions.feature_mC_levels('CDS_allc.tmp',features,
                                output='results/gene_methylation_levels.tsv',
                                cutoff=0,filter_features='gene',filter_chr=filter_chr)
    os.remove('CDS_allc.tmp')
    os.remove('f_tmp')
    os.remove('c_tmp')
else:
    print('No gene annotations found')
