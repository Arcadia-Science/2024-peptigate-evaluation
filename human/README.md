# Evaluate the performance of the peptigate workflow on the human transcriptome

This folder documents the steps we took to evaluate the peptigate workflow on the human RefSeq transcriptome.
This README shows how we obtained and preprocessed the data for peptigate and how we ran the peptigate workflow.
The [notebook](./20240319-human-txome-results.ipynb) in this directory provides an overview of the results of the peptigate run.

## Prepare the data and run peptigate

Download human transcriptome and predicted genes/proteins data
```
curl -JLO https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_000001405.40/download\?include_annotation_type\=GENOME_FASTA\&include_annotation_type\=GENOME_GFF\&include_annotation_type\=RNA_FASTA\&include_annotation_type\=CDS_FASTA\&include_annotation_type\=PROT_FASTA\&include_annotation_type\=SEQUENCE_REPORT\&hydrated\=FULLY_HYDRATED
```

Extract the specific files needed for peptigate:
```
unzip -p ncbi_dataset.zip ncbi_dataset/data/GCF_000001405.40/rna.fna > GCF_000001405.40_rna.fna
unzip -p ncbi_dataset.zip ncbi_dataset/data/GCF_000001405.40/cds_from_genomic.fna > GCF_000001405.40_cds_from_genomic.fna
unzip -p ncbi_dataset.zip ncbi_dataset/data/GCF_000001405.40/protein.faa > GCF_000001405.40_protein.faa
```

Make a peptigate config file:
```
input_dir: "inputs/"
output_dir: "outputs/human/"

orfs_amino_acids: "human/GCF_000001405.40_protein.faa"
orfs_nucleotides: "human/GCF_000001405.40_cds_from_genomic.fna"
contigs_shorter_than_r2t_minimum_length: "human/GCF_000001405.40_empty.fna"
contigs_longer_than_r2t_minimum_length: "human/GCF_000001405.40_rna.fna"
plmutils_model_dir: "inputs/models/plmutils/"
```

Run peptigate (from commit [`10efe0d`](https://github.com/Arcadia-Science/peptigate/pull/26/commits/10efe0d778fb47631aa7a6ce7cc286e8799c761a)).
We ran peptigate in the environment specified in the peptigate pipeline (`envs/dev.yml`).
```
snakemake --software-deployment-method conda -j 1 -k --configfile human_peptigate_config.yml
```

Peptigate results are in the `peptigate_results`.
We gzip compressed the files before adding them to this repository.

## Examining the outputs

We analyzed the peptigate peptide predictions in the notebook [20240319-human-txome-results.ipynb](./20240319-human-txome-results.ipynb). 
