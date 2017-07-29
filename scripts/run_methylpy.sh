#PBS -S /bin/bash
#PBS -q batch
#PBS -N methylpy
#PBS -l nodes=1:ppn=12:HIGHMEM
#PBS -l walltime=999:00:00
#PBS -l mem=100gb

echo "Starting"
cd $PBS_O_WORKDIR
sample=$(pwd | sed s/.*data\\/// | sed s/\\///)

#Download data
if ls fastq/*fastq.gz
then
	echo "Sequence data exists"
	cd fastq
	for i in *fastq.gz
	do
		gunzip "$i"
	done
	cd ../
elif ls fastq/*fastq
then
		echo "Unzipped sequence data exists"
else
	echo "No Sequence data, retrieving sequencing data"
	cd fastq
	module load python/3.5.1
	python3.5 ../../../scripts/download_fastq.py "$sample"
	module load sratoolkit/2.8.2-1
	for i in *sra
	do
		fastq-dump --gzip --split-3 "$i"
		rm "$i"
	done
	if ls fastq/*fastq.gz
	then
		for i in *fastq.gz
		do
			gunzip "$i"
		done
	fi
	cd ../
fi

#check if paired end and process accordingly
if ls fastq/SRR*_2.fastq
then
	if ls fastq/SRR*_2_rc.fastq
	then
		echo "Data is paired-end, already reverse complemented"
	else
		echo "Data is paired-end, trimming and reverse complementing"
		cd fastq
		for i in SRR*_2.fastq
		do
			output=$(echo "$i" | sed s/.fastq/_rc.fastq/)
			module load python/2.7.8
			time python /usr/local/apps/cutadapt/1.9.dev1/bin/cutadapt \
			-a AGATCGGAAGAGCGTCGTGTAGGGA -o tmp.fastq "$i"
			time /usr/local/apps/fastx/0.0.14/bin/fastx_reverse_complement \
			-i tmp.fastq -o tmp2.fastq
	    sed s/\ HWI/\.2\ HWI/g tmp2.fastq > "$output"
	    rm tmp.fastq tmp2.fastq
			gzip "$i"
		done
		cd ../
	fi
else
	echo "Data is single-end"
fi

#Map bisulfite data
cd methylCseq
module load python/2.7.8
echo "Running methylpy"
if ls ../fastq/SRR*_2_rc.fastq
then
	python ../../../scripts/run_methylpy.py "$sample" \
	"../fastq/*.fastq" "../ref/$sample" "10" "9" "AGATCGGAAGAGCACACGTCTGAAC" \
	"ChrL" > "$sample"_output.txt
else
	python ../../../scripts/run_methylpy.py "$sample" \
	"../fastq/*.fastq" "../ref/$sample" "10" "9" "AGATCGGAAGAGCTCGTATGCC" \
	"ChrL" > "$sample"_output.txt
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
cd ../

echo "Done"
