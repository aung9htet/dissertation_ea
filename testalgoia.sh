#!/bin/bash
#$ -l rmem=6G
#$ -pe openmp 10


module load apps/python/conda

source activate dissertation

python symmetric_mexpohd_multiprocessing.py
