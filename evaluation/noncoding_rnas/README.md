Check whether peptigate predicted that bona fide long non-coding RNAs are coding.

```
seqkit grep --pattern-file ../../peptigate/results/sORF/plmutils/plmutils_peptide_names.faa -o sorf_transcripts.fa ../../peptigate/running_peptigate/GCF_000001405.40_GRCh38.p14_rna.fna
grep "NR_001564.3" sorf_transcripts.fa # XIST
grep "NR_186242.1" sorf_transcripts.fa # HOTAIR
grep "NR_028272.1" sorf_transcripts.fa # NEAT1 (MENepsilon)
grep "NR_131012.1" sorf_transcripts.fa # NEAT1 (MENbeta)
```

Peptigate did not predict any of these transcripts to be coding.
