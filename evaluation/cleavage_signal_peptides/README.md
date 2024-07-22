# Determining whether predicted cleavage peptides (from DeepPeptide) that don't match peptides in databases have other traits that support their veracity.

We started by predicting whether parent proteins of cleavage peptides had signal peptides.
We used the DeepSig environment file defined in peptigate.
```
curl -JLO https://raw.githubusercontent.com/Arcadia-Science/peptigate/main/envs/deepsig.yml
mamba env create -n deepsig --file deepsig.yml
mamba activate deepsig
```

We then ran DeepSig on the parent (precursor) proteins for DeepPeptide-predicted cleavage peptides.
We also post-processed this file with the peptigate script.
```
gunzip ../../peptigate/results/cleavage/deeppeptide/deeppeptide_peptide_parents.faa.gz 
deepsig -f ../../peptigate/results/cleavage/deeppeptide/deeppeptide_peptide_parents.faa -o deeppeptide_peptide_parents.tmp -k euk
curl -JLO https://raw.githubusercontent.com/Arcadia-Science/peptigate/main/scripts/add_header_to_deepsig_tsv.py
python add_header_to_deepsig_tsv.py deeppeptide_peptide_parents.tmp deeppeptide_peptide_parents_deepsig.tsv
```

These results, as well as the results from propeptides predicted on the parent proteins, are analyzed in the [notebook](./20240719-check-cleavage-peptide-parent-signal-and-propeptides.ipynb) in this directory.
