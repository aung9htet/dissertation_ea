#!/bin/bash
#$ -l rmem=6G
#$ -pe openmp 10


module load apps/python/conda

source activate dissertation

python opt_ia_multiprocessing.py
