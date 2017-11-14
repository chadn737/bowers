# README

This github page contains the scripts used to map and call methylation in the paper ["Relationship between DNA methylation, biased duplicate gene retention, and biased mutation rates in plant genomes"]().

The entire methylation analysis of the paper should be able to be repeated by running the scripts on this github page. However, these scripts were originally designed to run on UGA's GACRC Sapelo cluster (2016). So slight modification to the scripts maybe required to make them compatible on other systems.

### Required Software and Modules

1. python3
2. pandas (python module)
3. scipy (python module)
4. numpy (python module)
5. pybedtools (python module)
6. biopython (python module)
7. urllib (python module)
8. Bedtools
9. bowtie & bowtie2
10. samtools
11. [methypy](https://github.com/yupenghe/methylpy) (python)
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

Best of luck.  
**Chad Niederhuth**  
Nov 13, 2017
