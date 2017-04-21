#PBS -S /bin/bash
#PBS -q batch
#PBS -N methylpy
#PBS -l nodes=1:ppn=12:HIGHMEM
#PBS -l walltime=999:00:00
#PBS -l mem=100gb

echo "Starting"
cd $PBS_O_WORKDIR
module load sratoolkit/2.8.0

#Download data
echo "Retrieving sequencing data"
cd ../fastq
module load python/3.5.1
python3.5 ../../../scripts/download_fastq.py "$i"
for i in *sra
do
	fastq-dump --gzip --split-3 "$i" 
	rm "$i"
done

#Map bisulfite data
cd ../methylCseq
module load python/2.7.8
python ../../../scripts/ run_methylpy.py "$sample" \
"../fastq/*.fastq" "../ref/$sample" "10" "9" "ChrL" \
> reports/"$sample"_output.txt

#Organize files
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

echo "Done"
