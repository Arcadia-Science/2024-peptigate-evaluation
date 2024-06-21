Check whether peptigate predicted peptides in *bona fide* long non-coding RNAs.
*Bona fide* long non-coding RNAs do not contain sORFs or any coding sequence.
Therefore, peptigate should not predict an sORF on these transcripts.
A frequent failure mode for sORF-encoded peptide annotation is that sORFs are too short to be detected by normal gene annotation software (typically 300 nucleotides/100 amino acids) and so the transcript is marked as non coding.
*Bona fide* long non-coding RNAs are not like these transcripts; they actually contain no coding sequence. 

```
seqkit grep --pattern-file ../../peptigate/results/sORF/plmutils/plmutils_peptide_names.faa -o sorf_transcripts.fa ../../peptigate/running_peptigate/GCF_000001405.40_GRCh38.p14_rna.fna
grep "NR_001564.3" sorf_transcripts.fa # XIST
grep "NR_186242.1" sorf_transcripts.fa # HOTAIR
grep "NR_028272.1" sorf_transcripts.fa # NEAT1 (MENepsilon)
grep "NR_131012.1" sorf_transcripts.fa # NEAT1 (MENbeta)
```

Peptigate did not predict any of these transcripts to be coding.
