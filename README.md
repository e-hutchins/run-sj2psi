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
 - `samples.txt` : user provided. Should match the parent directories for the SJ.out.tab files.

Directory structure:
```
.
├── star/
│   ├── sample1/
│   │   └── sample1.SJ.out.tab
│   ├── sample2/
│   │   └── sample2.SJ.out.tab
│   ├── sample3/
│   │   └── sample3.SJ.out.tab
```
## execution

```
SAMPLES=($(cat samples.txt))
#STAR_DIR=/path/to/your/star_parent_directory/
# for SAMPLE in "${SAMPLES[@]}"; do echo $SAMPLE; sbatch -J sj2psi_$SAMPLE --export=ALL,SAMPLE_NAME=${SAMPLE},STAR_DIR=${STAR_DIR} scripts/submit_sj2psi.sh ; sleep 1 ; done
```

## output
Outputs file in same directory as SJ.out.tab like so:

```
.
├── star/
│   ├── sample1/
│   │   └── sample1.SJ.out.tab
|   |   └── sample1.SJ.withPSIs.txt
│   ├── sample2/
│   │   └── sample2.SJ.out.tab
|   |   └── sample2.SJ.withPSIs.txt
│   ├── sample3/
│   │   └── sample3.SJ.out.tab
|   |   └── sample3.SJ.withPSIs.txt

```