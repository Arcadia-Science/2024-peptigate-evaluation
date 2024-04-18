# 2024-peptigate-evaluation

[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/projects/miniconda/en/latest/)

## Purpose

This repository assesses the accuracy of the [peptigate pipeline](https://github.com/Arcadia-Science/peptigate) by comparing peptide predictions from transcriptomes against orthogonal data sets (ribosome profiling, peptide databases, and peptidomics mass spectrometry).

## Installation and Setup

This repository uses conda to manage software environments and installations. You can find operating system-specific instructions for installing miniconda [here](https://docs.conda.io/projects/miniconda/en/latest/). After installing conda and [mamba](https://mamba.readthedocs.io/en/latest/), run the following command to create the pipeline run environment.

```{bash}
mamba env create -n pepeval --file envs/dev.yml
conda activate pepeval
```

## Overview

This reposity assess whether the [peptigate pipeline](https://github.com/Arcadia-Science/peptigate) predicts real peptides from transcriptome assemblies.
It does this by comparing the peptigate peptide predictions against three orthogonal data sources: ribosome profiling, peptide databases, and peptidomics mass spectrometry.
As described below in the description of the folder structure, this evaluation takes places in three separate folders, one per orthogonal data set type.
We provide a summary of the results in this main README, but the code, analysis, and details about the results are located in the README and notebooks of each sub-folder.

### Description of the folder structure

* [LICENSE](./LICENSE): specifies terms for re-use of the code in this repo.
* [README.md](./README.md): describes the contents of this repo and how to interact with it.
* [SRP074404](./SRP074404): contains code and results for the peptigate run on the spider mite transcriptome and comparison against a mass spec peptidomics run.
* [envs](./envs): documents conda software environments used for analyses in this repo.
* [human](./human): contains code and results for the peptigate run on the human RefSeq transcriptome and comparison against peptides in the database the Human Peptide Atlas.
* [riborf](./riborf): contains code and results for the peptigate run on the human RefSeq transcriptome and comparison against peptides predicted from a compendium of ribosomal profiling data.
* [.github](./.github), [.vscode](./.vscode), [Makefile](./Makefile), [pyproject.toml](./pyproject.toml): Control the developer behavior of the repository. 

### Data

See the README in each analysis folder for a description of the data and URLs for download. 

### Description of results

To understand how well peptigate predicts peptides, we performed three tests.
See the README and notebooks in each analysis folder for more details.
In each table, "Evidence peptide is real" means the peptide was either in the peptidomics data set (spider mite), the ribosome profiling data set (human riborf), or in the peptipedia peptide database (all three).

1. Run peptigate on the human transcriptome and compare against databases of peptides that contain human peptide predictions.
   For this test, we expected the sORF prediction to have a low true positive rate because we removed annotated sORFs before performing sORF prediction. See [this notebook](./human/20240319-human-txome-results.ipynb) for more details and results.
    
    | Peptide type | Prediction tool | Evidence peptide is real | Num peptides |
    | --- | --- | --- | --- |
    | cleavage | deeppeptide | evidence | 559 |
    | cleavage | deeppeptide | no evidence | 1122 |
    | cleavage | nlpprecursor | evidence | 91 |
    | cleavage | nlpprecursor | no evidence | 113 |
    | sORF | plmutils | evidence | 144 |
    | sORF | plmutils | no evidence | 2833 |

2. Run peptigate on the spider mite *T. urticae* with paired peptidomics data.
   In this test, the transcriptome ended up being incredibly low quality which hindered our ability to detect peptides.
   We think the high number of sORFs comes from the prediction of 3' and 5' UTR sORFs in fragmented transcripts.
   We usually remove transcripts that contain annotated genes prior to scanning for sORFs so these typically wouldn’t be detect (they usually regulate their own transcript so we made the executive decision to not detect them with peptigate).
   However, because the spider mite transcriptome was so fragmented, true gene-coding transcripts weren't annotated and thus weren't removed. 
   See [this notebook](./SRP074404/20240320-peptigate-against-peptidomics.ipynb) for more details and results.
     
    | Peptide Type | Prediction tool | Evidence peptide is real | Num peptides |
    | --- | --- | --- | --- |
    | cleavage | deeppeptide | evidence | 7 |
    | cleavage | deeppeptide | no evidence | 11 |
    | cleavage | nlpprecursor | evidence | 1 |
    | sORF | plmutils | evidence | 35 |
    | sORF | plmutils | no evidence | 2587 |

3. Run peptigate on the human transcriptome and compare against a large compendium of ribosomal profiling data.
   Ribosome profiling data is generated by sequencing fragments of mRNA that are protected by ribosomes, offering a snapshot of translation in action at a given moment.
   We compared the peptigate predictions from the human transcriptome against a recent re-analysis of a large compendium of human ribosome profiling data. 
   See [this notebook](./riborf/20240329-peptigate-vs-riborf-predictions.ipynb) for more details and results.
    
    | Peptide Type | Prediction tool | Evidence peptide is real | Num peptides |
    | --- | --- | --- | --- |
    | cleavage | deeppeptide | evidence | 1257 |
    | cleavage | deeppeptide | no evidence | 424 |
    | cleavage | nlpprecursor | evidence | 130 |
    | cleavage | nlpprecursor | no evidence | 74 |
    | sORF | plmutils | evidence | 164 |
    | sORF | plmutils | no evidence | 2364 |

From these tests, we observed that peptigate accurately predicts cleavage peptides.
The majority of cleavage peptides that were predicted in each test set had a hits against control databases (peptipedia in test 1, the mass spec peptidomic data in test 2, and ribosomal profiling data in test 3).
We take this as evidence that the when peptigate reports a cleavage peptide, there is strong evidence that that prediction is likely a real peptide.

We did not see the same hit level for against control databases for sORF predictions.
Some sORF peptide predictions did have hits in every data set, but the majority did not.
We also had far more sORF predictions than cleavage predictions in most test cases.
However, one reason for this is that we would expect to predict sORF that occur in 3' or 5' UTRs of coding sequences (these are SUPER common) if the transcript was a fragment at all, which is very common for transcriptome assemblies assembled from short read data.

Note that no gold standard data set exists for peptide prediction, which makes it difficult to assess the accuracy of the peptigate tool.
For example, we do not report traditional classification metrics like area under the curve, F1 score, etc.
The lack of gold standard data set highlights how little is known in the field of peptides.
One paper noted that only 300 peptides have confirmed bioactivity so far [10.1038/s41467-022-34031-z], indicating that this space is dramatically under explored.

### Compute Specifications

* Platform: x86_64-apple-darwin13.4.0 (64-bit)
* Running under: macOS Big Sur ... 10.16
* Ram: 64 GB

## Contributing

See how we recognize [feedback and contributions to our code](https://github.com/Arcadia-Science/arcadia-software-handbook/blob/main/guides-and-standards/guide-credit-for-contributions.md).

