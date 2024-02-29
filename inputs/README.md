## Getting peptide predictions from RNA-seq data

```
pysradb metadata --saveto SRP074404-metadata.tsv --detailed SRP074404
# cut grabs just the SRR identifier column. Tail -n +2 removes the header. The redirect saves the results in a file.
cut -f1 SRP074404-metadata.tsv | tail -n +2 > SRP074404-ids.csv
nextflow run nf-core/fetchngs -profile conda --input SRP074404-ids.csv --skip_fastq_download --outdir fetchngs
```
