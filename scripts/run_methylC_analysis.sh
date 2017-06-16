#PBS -S /bin/bash
#PBS -q batch
#PBS -N methylC_analysis
#PBS -l nodes=1:ppn=2:HIGHMEM
#PBS -l walltime=480:00:00
#PBS -l mem=300gb

cd $PBS_O_WORKDIR
sample=$(pwd | sed s/.*data\\/// | sed s/\\/.*//)
echo "Starting" "$sample"
module load anaconda/3-2.2.0
module load bedtools/2.23.0
mkdir results
python3.4 ../../../scripts/methylC_analysis.py "$sample"
