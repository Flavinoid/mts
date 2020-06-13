# Fetch FASTA data from Uniprot

To use this action you need to make sure that the `run.sh` script is executable

```sh
$ chmod 755 run.sh
```

to check that it works it is advisable to then run the following command

```sh
$ ./run.sh --dev
```

The `--dev` flag will use a file called [protein_ids_samples.csv](data/in/protein_ids_samples.csv). This file is a small selection of the full set of data [protein_ids.csv](data/in/protein_ids.csv).

Using the main file takes a while and generates a roughly 5mb output file.

After the data has been fetched from `Uniprot` and the resulting `csv` written to either `data/out/uniprot_results_sample.csv` or `data/out/uniprot_results.csv` a directory `/out/fasta` will be created that contains FASTA files suitable for uploading to ?.

## working with existing data

If you already have a `data/out/uniprot_results.csv` file and just want to generate the `FASTA` files for uploading - you can use the command.

```sh
$ ./generate_fasta_files.sh
```

Again you will need to make sure that it is executable. By default this will use the file `data/out/uniprot_results.csv` as input. If you call the command with the `--dev` flag (`./generate_fasta_files.sh --dev`) then it will read the file from `data/out/uniprot_results_sample.csv`.
