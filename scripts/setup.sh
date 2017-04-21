#PBS -S /bin/bash
#PBS -q batch
#PBS -N setup
#PBS -l nodes=1:ppn=2:rjsnode
#PBS -l walltime=999:00:00
#PBS -l mem=10gb

echo "Starting"
cd $PBS_O_WORKDIR
module load samtools/1.2

for i in Athaliana Bdistachyon Osativa Ppersica \
Ptrichocarpa Sbicolor Slycopersicum Vvinifera Zmays
do
	echo "Preparing $i"
	mkdir "$i"
	cd "$i"
	mkdir ref fastq methylCseq

	#Make index files
	cd ref
	echo "Downloading and prepping genome"
	module load python/3.5.1
	python3.5 ../../../scripts/download_genomes.py "$i"
	cat "$i".fa ../../../misc/ChrL.fa > tmp
	module load python/2.7.8
	python ../../../scripts/fix_fasta.py -i tmp -o "$i".fa
	rm tmp
	samtools faidx "$i".fa
	echo "Building index"
	python ../../../scripts/build_methylCseq_index.py "$i"
	cd ../../
	echo "$i done"
done
