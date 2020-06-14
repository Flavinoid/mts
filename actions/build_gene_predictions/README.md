# Mapping Protein-id predictions onto Genes

## cleaning up the Data

By now you should have the file [actions/upload_fasta_files/data/out/predictions.txt](../upload_fasta_files/data/out/predictions.txt)

```
$ ./run.sh
```

This script performs two steps. Firstly it will extract the protein-ids that are predicted as being a "Mitochondrial targeting". The output is then written to two files `/data/out/mito_targeting_proteinIDs.txt`. After this it will use the data in [./data/in/gene_and_associated_proteins.csv](./data/in/gene_and_associated_proteins.csv) in combination with the newly generated file to create the file [/data/out/predicated_mito_targeting_genes.txt](./data/out/predicated_mito_targeting_genes.txt).

The files are just normal text files with a name per row:

## note

the returned values from `targetP` look like: `sp_Q96RR1_PEO1_HUMAN`.
We use the `UniProtKB` section (`Q96RR1`) to link the protein-ids back to the file [./data/in/gene_and_associated_proteins.csv](./data/in/gene_and_associated_proteins.csv)

In general it seems like the long versions have the form

```
<sp|tr>_<UniProtKB>_<GENE_NAME>_<HUMAN|Hm>(_<number>)
```
