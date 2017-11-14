import os
import sys
import pybedtools as pbt
import pandas as pd
import itertools
import numpy as np
from scipy import stats

#interpret sequence context, taken from methylpy.utils
def expand_nucleotide_code(mc_type=["C"]):
    iub_dict = {"N":["A","C","G","T"],"H":["A","C","T"],"C":["C"],"G":["G"],"T":["T"],"A":["A"]}
    for type in mc_type[:]:
        type += "N" * (3 - len(type))
        mc_type.extend(["".join(i) for i in itertools.product(*[iub_dict[nuc] for nuc in type])])
    if "C" in mc_type:
        mc_type.extend(["CG", "CHG", "CHH","CNN"])
    if "CG" in mc_type:
        mc_type.extend(["CGN"])
    return mc_type

#filter allc file based on sequence context
def filter_context(allc,context=["C"]):
    a = pd.read_table(allc,dtype={'chr':str,'pos':int,'strand':str,'mc_class':str,
                      'mc_count':int,'total':int,'methylated':int})
    a = a[a.mc_class.isin(expand_nucleotide_code(context))]
    return a

def allc2bed(allc,context=["C"],bed=True):
    a = filter_context(allc,context)
    a['pos2'] = a.pos
    a['name'] = a.index
    a['score'] = "."
    a = a[['chr','pos','pos2','name','score','strand','mc_class','mc_count','total','methylated']]
    if bed is True:
        a = pbt.BedTool.from_dataframe(a)
    return a

#simple function for filtering gff files based on feature (gene, exon, mRNA, etc)
def feat_filter(x,feature):
    if feature:
        return x[2] == feature
    else:
        return x

#simple function for filtering gff files based on strand
def strand_filter(x,strand):
    return x.strand == strand

#simple function for filtering gff files based on chromosome
def chr_filter(x,chr):
    return x.chrom not in chr

#map methylation to features
def map2features(allc,features,genome_file,updown_stream=2000,first_feature=(),second_feature=(),filter_chr=[]):
    bed = pbt.BedTool(features).filter(feat_filter,first_feature).filter(chr_filter,filter_chr)
    flank_bed = pbt.bedtool.BedTool.flank(bed,g=genome_file,l=updown_stream,r=updown_stream,s=True).saveas('f_tmp')
    cds_bed = pbt.BedTool(features).filter(feat_filter,second_feature).filter(chr_filter,filter_chr).saveas('c_tmp')
    bed = cds_bed.cat(flank_bed, postmerge=False)
    mC_bed = allc2bed(allc)
    mapping = pbt.bedtool.BedTool.intersect(mC_bed,bed,wa=True)
    m = pd.read_table(mapping.fn, header=None, usecols = [0,1,5,6,7,8,9])
    m.columns = ['chr','pos','strand','mc_class','mc_count','total','methylated']
    m = m.drop_duplicates()
    m.to_csv('CDS_allc.tmp', sep='\t', index=False)

#Get feature methylation data
def feature_mC_levels(allc,features,output=(),cutoff=0,filter_features=(),filter_chr=[]):
    bed = pbt.BedTool(features).filter(feat_filter,filter_features).filter(chr_filter,filter_chr)
    mC_bed = allc2bed(allc)
    mapping = pbt.bedtool.BedTool.intersect(mC_bed,bed,wa=True,wb=True)
    m = pd.read_table(mapping.fn, header=None, usecols = [18,6,7,8,9])
    m = m.sort_values(by = 18,ascending=True)
    a = pd.DataFrame(columns=['Gene','CG_sites','mCG_sites','CG_reads','mCG_reads',
                              'CG_methylation_level','CHG_sites','mCHG_sites','CHG_reads',
                              'mCHG_reads','CHG_methylation_level','CHH_sites','mCHH_sites',
                              'CHH_reads','mCHH_reads','CHH_methylation_level','C_sites',
                              'mC_sites','C_reads','mC_reads','C_methylation_level'])
    name = "none"
    rCG = mrCG = CG = mCG = rCHG = mrCHG = CHG = mCHG = rCHH = mrCHH = CHH = mCHH = 0
    for c in m.itertuples():
        if name == "none":
            name = c[5]
            if int(c[3]) >= int(cutoff):
                if c[1].startswith("CN"):
                    continue
                elif c[1].startswith("CG"):
                    rCG = rCG + int(c[3])
                    mrCG = mrCG + int(c[2])
                    CG = CG + 1
                    mCG = mCG + int(c[4])
                elif c[1].endswith("G"):
                    rCHG = rCHG + int(c[3])
                    mrCHG = mrCHG + int(c[2])
                    CHG = CHG + 1
                    mCHG = mCHG + int(c[4])
                else:
                    rCHH = rCHH + int(c[3])
                    mrCHH = mrCHH + int(c[2])
                    CHH = CHH + 1
                    mCHH = mCHH + int(c[4])
        elif c[5] != name:
            a = a.append({'Gene':name, 'CG_sites':CG, 'mCG_sites':mCG,
                          'CG_reads':rCG, 'mCG_reads':mrCG,
                          'CG_methylation_level':str(np.float64(mrCG)/np.float64(rCG)),
                          'CHG_sites':CHG, 'mCHG_sites':mCHG, 'CHG_reads':rCHG,
                          'mCHG_reads':mrCHG, 'CHG_methylation_level':str(np.float64(mrCHG)/np.float64(rCHG)),
                          'CHH_sites':CHH, 'mCHH_sites':mCHH, 'CHH_reads':rCHH, 'mCHH_reads':mrCHH,
                          'CHH_methylation_level':str(np.float64(mrCHH)/np.float64(rCHH)),
                          'C_sites':(CG+CHG+CHH), 'mC_sites':(mCG+mCHG+mCHH),
                          'C_reads':(rCG+rCHG+rCHH), 'mC_reads':(mrCG+mrCHG+mrCHH),
                          'C_methylation_level':str(np.float64(mrCG+mrCHG+mrCHH)/np.float64(rCG+rCHG+rCHH))
                          },ignore_index=True)
            name = c[5]
            rCG = mrCG = CG = mCG = rCHG = mrCHG = CHG = mCHG = rCHH = mrCHH = CHH = mCHH = 0
            if int(c[3]) >= int(cutoff):
                if c[1].startswith("CN"):
                    continue
                elif c[1].startswith("CG"):
                    rCG = rCG + int(c[3])
                    mrCG = mrCG + int(c[2])
                    CG = CG + 1
                    mCG = mCG + int(c[4])
                elif c[1].endswith("G"):
                    rCHG = rCHG + int(c[3])
                    mrCHG = mrCHG + int(c[2])
                    CHG = CHG + 1
                    mCHG = mCHG + int(c[4])
                else:
                    rCHH = rCHH + int(c[3])
                    mrCHH = mrCHH + int(c[2])
                    CHH = CHH + 1
                    mCHH = mCHH + int(c[4])
        elif c[5] == name:
            if int(c[3]) >= int(cutoff):
                if c[1].startswith("CN"):
                    continue
                elif c[1].startswith("CG"):
                    rCG = rCG + int(c[3])
                    mrCG = mrCG + int(c[2])
                    CG = CG + 1
                    mCG = mCG + int(c[4])
                elif c[1].endswith("G"):
                    rCHG = rCHG + int(c[3])
                    mrCHG = mrCHG + int(c[2])
                    CHG = CHG + 1
                    mCHG = mCHG + int(c[4])
                else:
                    rCHH = rCHH + int(c[3])
                    mrCHH = mrCHH + int(c[2])
                    CHH = CHH + 1
                    mCHH = mCHH + int(c[4])
    a = a.append({'Gene':name, 'CG_sites':CG, 'mCG_sites':mCG,
                  'CG_reads':rCG, 'mCG_reads':mrCG,
                  'CG_methylation_level':str(np.float64(mrCG)/np.float64(rCG)),
                  'CHG_sites':CHG, 'mCHG_sites':mCHG, 'CHG_reads':rCHG,
                  'mCHG_reads':mrCHG, 'CHG_methylation_level':str(np.float64(mrCHG)/np.float64(rCHG)),
                  'CHH_sites':CHH, 'mCHH_sites':mCHH, 'CHH_reads':rCHH, 'mCHH_reads':mrCHH,
                  'CHH_methylation_level':str(np.float64(mrCHH)/np.float64(rCHH)),
                  'C_sites':(CG+CHG+CHH), 'mC_sites':(mCG+mCHG+mCHH),
                  'C_reads':(rCG+rCHG+rCHH), 'mC_reads':(mrCG+mrCHG+mrCHH),
                  'C_methylation_level':str(np.float64(mrCG+mrCHG+mrCHH)/np.float64(rCG+rCHG+rCHH))
                  },ignore_index=True)
    if output:
        a.to_csv(output, sep='\t', index=False)
    else:
        return a

#Script for doing False Discovery Rate 
def FDR(a,column,new_col):
    b=a[a[column] != "NaN"][column].sort_values(ascending=False)
    lp=len(b)
    x=list(reversed(range(1,lp+1)))
    y=np.minimum.accumulate([lp/i*j for i,j in zip(x,b)])
    z=[i if i < 1.0 else 1.0 for i in y]
    c=pd.DataFrame(z,columns=[new_col])
    c.index=b.index
    a=pd.concat([a,c],axis=1)
    return a

#Conduct binomial test to determine if genic methylation is significant
def gene_binom_test(df,cutoff=10,calc_baseline=True,mCG=(),mCHG=(),mCHH=(),output=()):
    a=pd.read_table(df,sep="\t")
    if calc_baseline:
        mCG=pd.DataFrame.sum(a['mCG_sites'])/pd.DataFrame.sum(a['CG_sites'])
        mCHG=pd.DataFrame.sum(a['mCHG_sites'])/pd.DataFrame.sum(a['CHG_sites'])
        mCHH=pd.DataFrame.sum(a['mCHH_sites'])/pd.DataFrame.sum(a['CHH_sites'])
    elif not mCG or not mCHG or not mCHH:
        print('Use must specify baseline mCG, mCHG, and mCHH levels')
        return
    a['CG_pvalue']=stats.binom.sf(a.mCG_sites-1,a.CG_sites,mCG)
    a['CG_pvalue']=[i if s >= cutoff else "NaN" for i,s in zip(a['CG_pvalue'],a['CG_sites'])]
    a=FDR(a,column="CG_pvalue",new_col="CG_qvalue")
    a['CHG_pvalue']=stats.binom.sf(a.mCHG_sites-1,a.CHG_sites,mCHG)
    a['CHG_pvalue']=[i if s >= cutoff else "NaN" for i,s in zip(a['CHG_pvalue'],a['CHG_sites'])]
    a=FDR(a,column="CHG_pvalue",new_col="CHG_qvalue")
    a['CHH_pvalue']=stats.binom.sf(a.mCHH_sites-1,a.CHH_sites,mCHH)
    a['CHH_pvalue']=[i if s >= cutoff else "NaN" for i,s in zip(a['CHH_pvalue'],a['CHH_sites'])]
    a=FDR(a,column="CHH_pvalue",new_col="CHH_qvalue")
    if output:
        a.to_csv(output, sep='\t', index=False)
    else:
        return a

#subscript to generate new start and end coordinates for gff file
def start_end_coordinates(features,genome_file,output=(),up=0,down=0,
                          use_three_prime=False):
    if isinstance(features, pd.DataFrame):
        a = features
        a[3] = np.int64(a[3])
        a[4] = np.int64(a[4])
    else:
        a = pd.read_table(features,header=None,sep="\t")
    if use_three_prime:
        a[3] = a[4]
    else:
        a[4] = a[3]
    a = pbt.BedTool.from_dataframe(a)
    if up != 0 or down != 0:
        a = pbt.bedtool.BedTool.flank(a,g=genome_file,l=up,r=down,s=True).saveas('tmp')
    if output:
        a.saveas(output)
        os.remove('tmp')
    else:
        return a

#Returns a modified gff file with only first X bps of sequence
def get_first_bps(features,genome_file,output=(),first_feature=(),
                  second_feature=(),up=0,down=0):
    a = pd.read_table(features,header=None,sep="\t")
    b = pd.DataFrame()
    d = 0
    for i, c in a.iterrows():
        if c[2] == first_feature and d == 0:
            d = 1
        elif c[2] == second_feature and d == 1:
            b = b.append(c)
            d = 0
    e = start_end_coordinates(b,genome_file,output=(),
                             up=up,down=down,use_three_prime=False)
    if output:
        e.saveas(output)
        os.remove('tmp')
    else:
        return e
