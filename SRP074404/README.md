# Evaluate the performance of the peptigate workflow on a spider mite transcriptome with a paired (ish) mass spec peptidomics data set

One way to validate the peptigate peptide predictions is to compare them against mass spectrometry peptidomics data.
Peptidomics is a specific mass spec technique that targets small protein sequences.
We identified a study where both transcriptomics and peptidomics were undertaken: ["A gene family coding for salivary proteins (SHOT) of polyphagous spider mite *Tetranychus urticae* exhibits fast host-dependent transcriptional plasticity"](https://doi.org/10.1094/MPMI-06-17-0139-R).
This folder compares the peptides predicted in the mass spec data vs. those predicted by peptigate.

This README covers preprocessing and analyses done to get peptide predictions.
The notebook [20240320-peptigate-against-peptidomics.ipynb](./20240320-peptigate-against-peptidomics.ipynb) then analyzes these files to compare peptigate predictions to peptidomics data.
 
## Getting peptide predictions from raw RNA-seq data

The study accession SRP074404 houses the spider mite RNA-seq data.
We use a combination of `pysradb` and `nf-core/fetchngs` to retrieve metadata about these samples in a format for the transcriptome assembly pipeline reads2transcriptome.
We ran this locally (MacBook Pro).

```
pysradb metadata --saveto SRP074404-metadata.tsv --detailed SRP074404
# cut grabs just the SRR identifier column. Tail -n +2 removes the header. The redirect saves the results in a file.
cut -f1 SRP074404-metadata.tsv | tail -n +2 > SRP074404-ids.csv
nextflow run nf-core/fetchngs -profile conda --input SRP074404-ids.csv --skip_fastq_download --outdir fetchngs
```
Next, I added the column `assembly_group` and back-filled the library name columns.

Then, I ran reads2transcriptome using Nextflow Tower.
```
nextflow run 'https://github.com/Arcadia-Science/reads2transcriptome'
		 -name crazy_torricelli_2
		 -params-file 'https://api.tower.nf/ephemeral/LXFinIj6RZjMzFSh_LNtvA.json'
		 -with-tower
		 -r 69f852567d1f459f1151c86e8dac4673634358e6
		 -profile docker
```

Using the parameters documented in `SRP074404_reads2transcriptome_parameters.json`.

The reads2transcriptome run was interupted during the evaluation step, so I ran transdecoder to predict ORFs.
```
aws s3 cp s3://arcadia-reads2transcriptome/peptigate-evaluation-gilad3/SRP074404/results/decontaminate/subseq_clean/illumina_top_contigs.fa.gz .
gunzip illumina_top_contigs.fa
mv illumina_top_contigs.fa SRP074404_contigs.fa

TransDecoder.LongOrfs -t SRP074404_contigs.fa --output_dir SRP074404/transdecoder/
TransDecoder.Predict -t SRP074404_contigs.fa --output_dir SRP074404/transdecoder/
```

Then, I merged the contigs files together from the reads2transcriptome outputs:
```
aws s3 cp s3://arcadia-reads2transcriptome/peptigate-evaluation-gilad3/SRP074404/results/merge_transcriptomes/preprocess/split_trinity/PRJNA320686_trinity.short.fa.gz .
aws s3 cp s3://arcadia-reads2transcriptome/peptigate-evaluation-gilad3/SRP074404/results/merge_transcriptomes/preprocess/split_rnaspades/PRJNA320686_rnaspades.short.fa.gz .
cat PRJNA320686*fa.gz > SRP074404_short_contigs.fa.gz
gunzip SRP074404_short_contigs.fa.gz
cat  SRP074404_r2t/SRP074404_contigs.fa > SRP074404_all_contigs.fa
```

Upon inspection of this file, there were no short contigs from this reads2transcriptome run.
(Note -- short contigs are the very short contigs [<75bp] that are filtered out by r2t but written to a file in case a user wants to see these very short things. There were none of these super short contigs. There _were_ some normal contigs in the default assembly output, which is what we ran peptigate on.)

These files were supplied to peptigate.

We made the following config file:

```
input_dir: "inputs/"
output_dir: "outputs/SRP074404/"

contigs: "SRP074404_r2t/SRP074404_all_contigs.fa"
orfs_amino_acids: "SRP074404_r2t/SRP074404_contigs.fa.transdecoder.pep"
orfs_nucleotides: "SRP074404_r2t/SRP074404_contigs.fa.transdecoder.cds"
plmutils_model_dir: "inputs/models/plmutils/"
```

And ran peptigate with the following command (from commit hash [37dacf](https://github.com/Arcadia-Science/peptigate/commit/37dacf77833e1188b831025416d3bde00edfdcc4)):
```
snakemake --software-deployment-method conda -j 2 -k --configfile SRP074404_peptigate_config.yml
```

We then gzip'd the resulting prediction and annotation TSV files:
```
gzip *tsv
```

Results are in the `results/SRP074404` directory.

## Comparing peptigate peptide predictions against peptidomics data

We downloaded peptidomics peptide predictions using the following code:
```
mkdir peptidomics
curl -JLo peptidomics/pep_20160811_crap_gen_simple_correct.fasta https://ftp.pride.ebi.ac.uk/pride/data/archive/2017/09/PXD006385/pep_20160811_crap_gen_simple_correct.fasta
```

There were 19,202 mass spec-predicted peptides in this file.
```
grep ">" peptidomics/pep_20160811_crap_gen_simple_correct.fasta | wc -l
```

We made a BLAST database of the peptidomics results
```
makeblastdb -in peptidomics/pep_20160811_crap_gen_simple_correct.fasta -dbtype prot -out peptidomics/pep_20160811_crap_gen_simple_correct
```

And BLASTp'd the peptigate peptide predictions against the mass spec peptidomics database.
```
mkdir blastp
gunzip ../results/SRP074404/peptides.faa.gz
blastp -db peptidomics/pep_20160811_crap_gen_simple_correct -query ../results/SRP074404/peptides.faa -out blastp/peptigate_sequences_vs_peptidomics_blastp.tsv -max_target_seqs 5 -outfmt "6 qseqid qlen qseq sseqid slen sseq pident length mismatch gapopen qstart qend sstart send evalue bitscore"
```

We also did the opposite -- tBLASTn'd the peptidomics MS data against the transcripts in the assembled transcriptome.
There's a chance we don't see a peptide because it didn't assemble, not because peptigate failed to predict it.
```
makeblastdb -in SRP074404_r2t/SRP074404_contigs.fa -dbtype nucl -out SRP074404_r2t/SRP074404_contigs
```

```
mkdir tblastn
tblastn -db SRP074404_r2t/SRP074404_contigs -query peptidomics/pep_20160811_crap_gen_simple_correct.fasta -out tblastn/peptidomics_vs_transcriptome_tblastn.tsv -max_target_seqs 5 -outfmt "6 qseqid qlen qseq sseqid slen sseq pident length mismatch gapopen qstart qend sstart send evalue bitscore"
```

We analyze these results in [20240320-peptigate-against-peptidomics.ipynb](./20240320-peptigate-against-peptidomics.ipynb)
