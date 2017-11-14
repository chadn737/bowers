#PBS -S /bin/bash
#PBS -q batch
#PBS -N methylpy
#PBS -l nodes=1:ppn=12:HIGHMEM
#PBS -l walltime=999:00:00
#PBS -l mem=100gb

export TMPDIR=$PBS_O_WORKDIR
export TMP=$PBS_O_WORKDIR
export TEMP=$PBS_O_WORKDIR

echo "Starting"
cd $PBS_O_WORKDIR
sample=$(pwd | sed s/.*data\\/// | sed s/\\///)
refC=$(grep $sample ../../misc/Samples.csv | cut -d ',' -f3)

#Download data
cd fastq
if ls *fastq.gz || ls *fastq
then
	echo "Sequence data is already downloaded"
else
	echo "Downloading sequencing data"
	#Download data
	module load python/3.5.1
	python3.5 ../../../scripts/download_fastq.py "$sample"
	#fastq-dump
	module load sratoolkit/2.8.2-1
	for i in *sra
	do
		fastq-dump --gzip --split-3 "$i"
		rm "$i"
	done
fi

#Unzip data
echo "Uncompressing fastq files"
for i in *fastq.gz
do
	gunzip "$i"
done

#Combine fastq files if more than one pair
if [ $(ls *_2.fastq | wc -l) -gt 1 ]
then
	echo "Combining fastq files"
	cat SRR[0-9]*_1.fastq > SRR_1.fastq
	rm SRR[0-9]*_1.fastq
	cat SRR[0-9]*_2.fastq > SRR_2.fastq
	rm SRR[0-9]*_1.fastq
fi

#Run methylpy
cd ../methylCseq
echo "Running methylpy"
module load python/2.7.8
module load bowtie2/2.2.9
if ls ../fastq/SRR*_2.fastq
then
	echo "Data is paired-end"
	index=$(ls ../ref/*fa.fai | sed s/.fa.fai//)
	python ../../../scripts/run_methylpy_pe.py "$sample" \
	"../fastq/*_1.fastq" "../fastq/*_2.fastq" "$index" \
  	"10" "9" "AGATCGGAAGAGCACACGTCTGAAC" "AGATCGGAAGAGCGTCGTGTAGGGA" \
	"$refC" > "$sample"_output.txt
else
	echo "Data is single-end"
	index=$(ls ../ref/*fa.fai | sed s/.fa.fai//)
	python ../../../scripts/run_methylpy.py "$sample" \
	"../fastq/*.fastq" "$index" "10" "9" "AGATCGGAAGAGCTCGTATGCC" \
	"$refC" > "$sample"_output.txt
fi

#Organize files
echo "Organizing and cleaning up"
rm *mpileup* *.bam *.bam.bai
mkdir tmp
head -1 allc_"$sample"_ChrL.tsv > tmp/header
for i in allc_"$sample"_*
do
	sed '1d' "$i" > tmp/"$i"
done
tar -cjvf "$sample"_allc.tar.bz2 allc_"$sample"_*
rm allc_*
cd tmp
rm allc_"$sample"_ChrL.tsv allc_"$sample"_ChrC.tsv
cat header allc_* > ../"$sample"_allc_total.tsv
cd ../
rm -R tmp
tar -cjvf "$sample"_allc_total.tar.bz2 "$sample"_allc_total.tsv
cd ../fastq
for i in *fastq
do
	gzip "$i"
done

echo "Done"
