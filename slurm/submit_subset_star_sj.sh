#!/bin/bash
#SBATCH --partition=quick,norm
#SBATCH --cpus-per-task=1
#SBATCH --mem=42G
#SBATCH --time=03:00:00

#execute as so:
#SAMPLES=($(cat ${PROJECT_DIR}/samples.txt))
#STAR_DIR=/path/to/your/star_parent_directory/
# for SAMPLE in "${SAMPLES[@]}"; do echo $SAMPLE; sbatch -J sj2psi_$SAMPLE --export=ALL,SAMPLE_NAME=${SAMPLE},STAR_DIR=${STAR_DIR},CE_INPUT_FILE=data/CE_junctions_in_Ed_Lee_data.csv ; sleep 1 ; done

#load modules
module load python/3.10 || exit 1

# Get the sample name from the command line argument
INPUT_FILE="${SAMPLE_NAME}.SJ.withPSIs.txt"
CE_INPUT_FILE=${CE_INPUT_FILE}
OUTPUT_FILE="${SAMPLE_NAME}.SJ.CE.subset.txt"

#cd into the directory with the input file
cd ${STAR_DIR}
cd ${SAMPLE_NAME}

# Run the Python script
python3 scripts/subset_star_sj.py --sj ${INPUT_FILE} --ce ${CE_INPUT_FILE} --out ${OUTPUT_FILE}