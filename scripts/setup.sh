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

	Make index files
	cd ref
	echo "Downloading and prepping genome"
	module load python/3.5.1
	python3.5 ../../../scripts/download_genomes.py "$i"
	sed -i s/gi\|1/ChrC/g "$i"_ChrC.fa
	cat "$i".fa "$i"_ChrC.fa ../../../misc/ChrL.fa > tmp
	module load python/2.7.8
	python ../../../scripts/fix_fasta.py -i tmp -o "$i".fa
	rm tmp
	samtools faidx "$i".fa
	cut -f1,2 "$i".fa.fai > "$i".genome
	echo "Building index"
	lib=$(grep $i ../../../misc/Samples.csv | cut -d ',' -f4)
	if [ $lib -eq 2 ]
	then
		python ../../../scripts/build_methylCseq_index_pe.py "$i"
	else
		python ../../../scripts/build_methylCseq_index.py "$i"
	fi
	echo "$i done"
done
