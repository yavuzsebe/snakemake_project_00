# Snakemake workflow example for data preprocessing and visualization

# This Snakefile defines rules for preprocessing data and generating visualizations.
# It assumes that the data files are in the 'data' directory and the scripts for preprocessing and visualization are in the 'scripts' directory.

# To run this workflow, you can create a conda environment using the provided environment.yml file and then run Snakemake with the following commands:

# cd ~/snakemake_project_00
# conda env create -n snakemakeDummyEnv -f envs/environment.yml
# conda activate snakemakeDummyEnv
# snakemakeDummyEnv --cores 1 -s Snakefile

import glob

datasets = [f.split("/")[-1].replace(".csv", "") for f in glob.glob("data/*.csv")]

rule all:
    input:
        expand("results/PCA_{data}.png", data=datasets),
        expand("results/Heatmap_{data}.png", data=datasets),
        expand("results/Boxplot_{data}.png", data=datasets),
        expand("results/miscGraph_{data}.png", data=datasets),
        expand("results/Summary_{data}.txt", data=datasets),
        expand("results/PVAL_{data}.txt", data=datasets)

rule preprocess:
    input:
        "data/{data}.csv"
    output:
        "data/preprocessed_{data}.csv"
    shell:
        "python scripts/preprocess.py {input} {output}"

rule visualize:
    input:
        "data/preprocessed_{data}.csv"
    output:
        "results/PCA_{data}.png",
        "results/Heatmap_{data}.png",
        "results/Boxplot_{data}.png",
        "results/miscGraph_{data}.png",
        "results/Summary_{data}.txt",
        "results/PVAL_{data}.txt"
    shell:
        "python scripts/visualize.py {input} results/" 