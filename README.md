# run-sj2psi
runs [sj2psi](https://github.com/olgabot/sj2psi) across a set of samples; outputs .csv file

## sj2psi install
```
git clone git@github.com:olgabot/sj2psi
cd sj2psi
pip install .
```

## files
 - `run_sj2psi.py` : runs sj2psi and outputs a .csv file
 - `submit_sj2psi.sh` : submits above python script to slurm cluster

## execution
assumes you have a `samples.txt` file that contains sample IDs. This should match the parent directory for the SJ.out.tab file.

.
├── star/
│   ├── sample1/
│   │   └── sample1.SJ.out.tab
│   ├── sample2/
│   │   └── sample2.SJ.out.tab
│   ├── sample3/
│   │   └── sample3.SJ.out.tab

```
SAMPLES=($(cat samples.txt))
#STAR_DIR=/path/to/your/star_parent_directory/
# for SAMPLE in "${SAMPLES[@]}"; do echo $SAMPLE; sbatch -J sj2psi_$SAMPLE --export=ALL,SAMPLE_NAME=${SAMPLE},STAR_DIR=${STAR_DIR} scripts/submit_sj2psi.sh ; sleep 1 ; done
```