# README

This github page contains the scripts used to map and call methylation in the paper ["Relationship between DNA methylation, biased duplicate gene retention, and biased mutation rates in plant genomes"]().

The entire methylation analysis of the paper should be able to be repeated by running the scripts on this github page. However, these scripts were originally designed to run on UGA's GACRC Sapelo cluster (2016). So slight modification to the scripts maybe required to make them compatible on other systems.

### Required Software and Modules

1. python 3 (methylC analysis)
2. python 2 (for methylpy)
2. pandas (python module)
3. scipy (python module)
4. numpy (python module)
5. pybedtools (python module)
6. biopython (python module)
7. urllib (python module)
8. Bedtools
9. bowtie & bowtie2
10. samtools
11. [methypy](https://github.com/yupenghe/methylpy) (originally used version < 1.0)
12. Unix environment
13. Probably something I'm missing...

### Running analysis

1. Clone this repository and make sure all required software is installed.
2. cd Bowers-Gene-Duplication-Methylation
3. mkdir data
4. cd data
5. bash ../scripts/setup.sh

For each species' directory in the data directory

6. cd <species dir>
7. bash ../../scripts/run_methylpy.sh
8. cd methylCseq
9. bash ../../../scripts/run_methylC_analysis.sh

Rerunning the entire analysis will take a very long time and uses a lot of memory. Rather than running it from the command line, I'd recommend submitting the various scripts as jobs.

### Notes

1. When I originally ran the analysis I was using an older version of methylpy that I ran with python 2. Some of my other python scripts (fix_fasta.py) also used python 2. Later analysis steps use python 3. I have since then switched entirely to using python 3 and use later versions of methylpy. For anyone trying to redo this analysis with newer versions of methylpy (1.0 and later) I'd recommend double checking all the arguments and modifying the scripts appropriately.
2. run_call_mc.sh and call_mc.sh are not required to run the analysis. These scripts are for restarting the methylpy pipeline after the mapping step in case it was interrupted or to change the unmethylated reference chromosome. 

Best of luck.  
**Chad Niederhuth**  
Nov 13, 2017
