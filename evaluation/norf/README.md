# Compare peptigate human peptide predictions against nORF predictions

A recent paper, ["A platform for curated products from novel open reading frames prompts reinterpretation of disease variants"](https://doi.org/10.1101/gr.263202.120) compiled human sORF predictions that have support from mass spectrometry or ribosomal profiling databases.
The authors termed their dataset ["novel ORFs" (nORFs)](https://norfs.org/), representing classes of small open reading frames: upstream ORFs (uORFs), downstream ORFs (dORFs), short ORFs (sORFs), small ORFs (smORFs), and alterantive ORFs (altORFs).
They provide the sequnces of these ORFs as well as their location relative to other annotated regions of the human genome:
> From the 194,407 nORFs, we found that 98,577 (50.7%) fully overlap canonical CDSs, 31,361 (16.1%) overlap CDSs and intron regions, 28,067 (14.4%) overlap 5′ UTRs, 5509 (2.8%) overlap 3′ UTRs, 19,909 (10.2%) overlap ncRNAs, and 4836 (2.5%) fully map to intronic or intergenic regions.

Peptigate is set up to detect sORFs that occur in ncRNAs (19,909) and that fully map to intronic or intergenic regions (4,836), meaning the peptigate predictions should have overlap with 24,745 predictions recorded in the nORF database.
Because transcriptome assembly and annotation is noisey, we also anticipate nominal overlap with predictions in the other categories.
In this directory, we compare the peptigate peptide predictions against the nORF predictions.

## Retrieve and format the nORF sequences

```{bash}
conda activate pepeval
```

Two files contain the information we will work with.
The GTF file contains transcript names and sequences, while a TSV file contains classification information.

```{bash}
# download nORF names & amino acid sequences
curl -JLo nORFsDB.1.1.gtf https://firebasestorage.googleapis.com/v0/b/phoenix-6686b.appspot.com/o/nORFsDB.1.1.gtf?alt=media&token=a3e41fe4-b1e5-4002-9384-b9d48bd5e25d
# download nORF location annotations
curl -JLo nORFsDB.1.1.classification.tsv https://firebasestorage.googleapis.com/v0/b/phoenix-6686b.appspot.com/o/nORFsDB.1.1.classification.tsv?alt=media&token=2c60916b-92ab-41a0-abe1-7519ccd1552c
```

The R script included in this directory combines these two files and outputs two TSV files.
The first contains two columns and reports the sequence name and amino acid sequence.
The second contains all metadata.
```{bash}
Rscript combine-norf-data.R --gtf nORFsDB.1.1.gtf --tsv nORFsDB.1.1.classification.tsv --output nORFsDB.1.1
```

Convert the two column TSV file to an amino acid FASTA file.
```{bash}
seqkit tab2fx nORFsDB.1.1_amino_acid.tsv -o nORFsDB.1.1.faa --comment-line-prefix novel_orf_id
```

## Compare the peptigate sORF predictions against the nORF sequences

We compared the peptigate peptide predictions against the nORF predictions by BLASTp-ing the peptigate predictions against the nORF predictions.
The peptigate results are located in the ../../peptigate/results folder.

First, we made a blast database of the nORF sequences.

```{bash}
makeblastdb -in nORFsDB.1.1.faa -dbtype prot -out nORFsDB.1.1.faa
```

Then, we BLAST'd the peptigate predictions against the nORF sequences
```{bash}
gunzip ../../peptigate/results/predictions/peptides.faa.gz
blastp -db nORFsDB.1.1.faa -query ../../peptigate/results/predictions/peptides.faa -out peptigate_sequences_vs_norf_blastp.tsv -max_target_seqs 5 -outfmt "6 qseqid qlen qseq sseqid slen sseq pident length mismatch gapopen qstart qend sstart send qcovhsp evalue bitscore"
```
