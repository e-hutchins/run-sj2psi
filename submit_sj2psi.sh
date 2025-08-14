#!/bin/bash
#SBATCH --partition=quick,norm
#SBATCH --cpus-per-task=1
#SBATCH --mem=42G
#SBATCH --time=03:00:00
#SBATCH -o /data/hutchinsed/run_logs/slurm.%J.%x.out

#execute from the results/star directory as so:
#SAMPLES=($(cat /data/CARD_AA/users/hutchinsed/2024_ROSMAP_RNAseq_TDP43/samples.txt))
# for SAMPLE in "${SAMPLES[@]}"; do echo $SAMPLE; sbatch -J sj2psi_$SAMPLE --export=ALL,SAMPLE_NAME=${SAMPLE} /data/hutchinsed/scripts/submit_sj2psi.sh ; sleep 1 ; done

#load modules
module load python/3.10 || exit 1

# Get the sample name from the command line argument
INPUT_FILE="${SAMPLE_NAME}.SJ.out.tab"
OUTPUT_FILE="${SAMPLE_NAME}.SJ.withPSIs.txt"

#cd into the directory with the input file
cd ${SAMPLE_NAME}

# Run the Python script
python3 /data/hutchinsed/scripts/run_sj2psi.py $INPUT_FILE $OUTPUT_FILE

cd ..