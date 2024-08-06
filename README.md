# Evaluating the results of the peptigate peptide prediction pipeline

[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/projects/miniconda/en/latest/)

## Purpose

This repository assesses the accuracy of the [peptigate pipeline](https://github.com/Arcadia-Science/peptigate) by comparing peptide predictions from the human transcriptomes against orthogonal data sets (ribosome profiling, peptide databases, and peptidomics mass spectrometry).

For more information, see the pub, ["Predicting bioactive peptides from transcriptome assemblies with the peptigate workflow."](https://doi.org/10.57844/arcadia-6500-9be8).

## Installation and Setup

This repository uses conda to manage software environments and installations. You can find operating system-specific instructions for installing miniconda [here](https://docs.conda.io/projects/miniconda/en/latest/). After installing conda and [mamba](https://mamba.readthedocs.io/en/latest/), run the following command to create the pipeline run environment.

```{bash}
mamba env create -n pepeval --file envs/dev.yml
conda activate pepeval
```

The arcadiathemeR R package isn't available to install via conda.
After activating the conda environment, use the following Rscript to install it.
```
Rscript scripts/install_arcadiathemer.R
```

The notebooks can also be run using the same environment.

## Overview

This reposity assess whether the [peptigate pipeline](https://github.com/Arcadia-Science/peptigate) predicts real peptides from the human transcriptome assembly.
It does this by comparing the peptigate peptide predictions against four orthogonal data sources: ribosome profiling, peptide databases, *bona fide* long non-coding RNAs, and strength of translation initiation sequences (Kozak sequences).
See the README and notebook in each sub-folder for a description of the analysis and results of each comparison.
Note that each notebook name is prepended with its creation date.

### Description of the folder structure

* [LICENSE](./LICENSE): specifies terms for re-use of the code in this repo.
* [README.md](./README.md): describes the contents of this repo and how to interact with it.
* [envs/](./envs): documents conda software environments used for analyses in this repo.
* [evaluation/](./evaluation): contains code, notebooks, documentation, and results for comparing the peptigate results against orthogonal data sets.
    * [kozak_scores/](./evaluation/kozak_scores): compares the strength of Kozak sequences (translation initiation sequences) in peptigate-predicted peptides against TransDecoder-predicted open reading frames in the human transcriptome.
    * [noncoding_rnas/](./evaluation/noncoding_rnas): tests whether peptigate predicted peptides from any *bona fide* long non-coding RNAs.
    * [peptipedia/](./evaluation/peptipedia): compares the peptigate peptide predictions against [Peptipedia](https://app.peptipedia.cl/), a large database of bioactive peptide sequences. 
    * [riborf/](./evaluation/riborf): compares the human transcriptome sORF-encoded peptides predicted by peptigate against open reading frames predicted by the tool ribORF from over 600 human ribosomal profiling data sets. 
* [peptigate/](./peptigate): contains documentation of how we ran peptigate on the human RefSeq transcriptome as well as results files output by peptigate.
* [.github/](./.github), [.vscode/](./.vscode), [.gitignore](./.gitignore), [.pre-commit-config.yml](./.pre-commit-config.yml), [Makefile](./Makefile), [pyproject.toml](./pyproject.toml): Control the developer behavior of the repository. 

### Data

This repository predicts peptides in the [human RefSeq transcriptome](https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_rna.fna.gz).
All peptide predictions (the results of running peptigate) are in the [peptigate results](./peptigate/results/) folder.
Download instructions for other auxiliary files required to reproduce the results in this repository are located in analysis-specific READMEs.

### Compute Specifications

* Platform: x86_64-apple-darwin13.4.0 (64-bit)
* Running under: macOS Big Sur ... 10.16
* Ram: 64 GB

## Contributing

See how we recognize [feedback and contributions to our code](https://github.com/Arcadia-Science/arcadia-software-handbook/blob/main/guides-and-standards/guide-credit-for-contributions.md).

