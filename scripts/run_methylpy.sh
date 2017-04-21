#PBS -S /bin/bash
#PBS -q batch
#PBS -N methylpy
#PBS -l nodes=1:ppn=12:HIGHMEM
#PBS -l walltime=999:00:00
#PBS -l mem=100gb

echo "Starting"
cd $PBS_O_WORKDIR
mkdir ref fastq methylCseq

#Make index files
cd ref
python ../../scripts/download_genomes.py "$i"
cat "$i".fa ../../../misc/ChrL.fa > ref/tmp
python ../../../scripts/fix_fasta.py -i tmp -o "$i".fa
samtools faidx "$i".fa
python ../../../scripts/build_index.py "$i"

#Download data
cd ../fastq
python ../../../scripts/download_fastq.py "$i"
#SRA

#Map bisulfite data
cd ../methylCseq
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
