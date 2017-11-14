#PBS -S /bin/bash
#PBS -q batch
#PBS -N call_mc
#PBS -l nodes=1:ppn=12:HIGHMEM
#PBS -l walltime=999:00:00
#PBS -l mem=100gb

cd $PBS_O_WORKDIR
sample=$(pwd | sed s/\\/methylCseq// | sed s/^.*\\///)
index=$(ls ../ref/*fa.fai | sed s/.fa.fai//)
module load python/2.7.8
echo "methylpy was previously interrupted" >> "$sample"_output.txt
echo "Resuming calling of methylated cytosines" >> "$sample"_output.txt
python ../../../scripts/call_mc.py "$sample"_processed_reads_no_clonal.bam \
"$sample" "$index".fa "ChrC" "10" "9" >> "$sample"_output.txt

#Format allc files
echo "Formatting allc files"
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
cd ..
rm -R tmp
tar -cjvf "$sample"_allc_total.tar.bz2 "$sample"_allc_total.tsv
cd ../

#Cleanup directory
echo "Cleaning up intermediate files"
rm *mpileup* *.bam *.bam.bai

#Compress fastq files
echo "Compressing fastq files"
cd ../fastq/methylCseq
rm *_rc.fastq
for i in *fastq
do
  gzip "$i"
done

echo "done"
