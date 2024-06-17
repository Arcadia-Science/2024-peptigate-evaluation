This README documents how we ran peptigate on the human transcriptome to produce the files in the [results](../results/) folder.
First, we prepared the human transcriptome for input into peptigate.
We downloaded the transcriptome and then annotated it with TransDecoder.
We recognize that this under utilizes the existing annotations for the human transcriptome.
However, TransDecoder is the recommended way to annotate a transcriptome before predicting peptides with peptigate, so we annotated it this way.

```
conda activate pepeval
mamba install transdecoder=5.7.1
curl -JLO https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_rna.fna.gz
gunzip GCF_000001405.40_GRCh38.p14_rna.fna.gz
TransDecoder.LongOrfs -t GCF_000001405.40_GRCh38.p14_rna.fna --output_dir transdecoder/
TransDecoder.Predict -t GCF_000001405.40_GRCh38.p14_rna.fna_contigs --output_dir transdecoder/
```

We then used the following config file to run peptigate:
```
input_dir: "inputs/"
output_dir: "outputs/human_transdecoder"
contigs: "input_data/human_transdecoder/GCF_000001405.40_GRCh38.p14_rna.fna"
orfs_amino_acids: "input_data/human_transdecoder/GCF_000001405.40_GRCh38.p14_rna.fna.transdecoder.pep"
orfs_nucleotides: "input_data/human_transdecoder/GCF_000001405.40_GRCh38.p14_rna.fna.transdecoder.cds"
plmutils_model_dir: "inputs/models/plmutils/"
```

And used this command to start peptigate:
```
snakemake --software-deployment-method conda -j 1 --configfile human_transdecoder_peptigate_config.yml
```

We ran peptigate from commit [411614fde6ed39439abaee5247bb6762ef82d4d5](https://github.com/Arcadia-Science/peptigate/commit/411614fde6ed39439abaee5247bb6762ef82d4d5).
We ran the pipeline on an AWS EC2 instance type `g4dn.2xlarge` running AMI Deep Learning Base OSS Nvidia Driver GPU AMI (Ubuntu 20.04) 20240122 (AMI ID ami-07eb000b3340966b0).
