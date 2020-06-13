# mts

MTS prediction

## Setup

After cloning this repo you want to run

```sh
source ./init.sh
```

## Use

The process of generating the graphs has been broken down into a sequence of [actions](actions).

The initial action [fetch_fasta_data_from_uniprot](actions/fetch_fasta_data_from_uniprot) assumes that you have some initial `input` data. Currently this data is hardcoded in the file [protein_ids.csv](actions/fetch_fasta_data_from_uniprot/in/protein_ids.csv).

An `action` directory normally contains a `run.sh` script that guides you through that step. There will also be a `README.md` file that will provide you with more information.

The three main steps required to generate the data required for creating the visualizations are the following.

1. [fetch_fasta_data_from_uniprot](actions/fetch_fasta_data_from_uniprot)
2. [upload_fasta_files](actions/upload_fasta_files)
3. [build_protein_predictions](actions/build_protein_predictions)

every new step builds upon the data returned by the previous ones.

Once the prediction files have been created it is possible to start with the visualizations and analysis.
