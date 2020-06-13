
function prompt_if_exists () {
    if [ -f "${1}" ]; then
        printf "It looks like the file '%s' already exists.\nAre you sure you want to continue?\n" "${1}"
    fi
}

function explain_read_write () {
    printf "running in dev mode: this will read from '%s' and write to '%s'\n" "${1}" "${2}"
}

if [ "${1}" = "--dev" ]; then     
    INFILE="protein_ids_sample.csv"
    OUTFILE="uniprot_results_sample.csv"
else
    echo "running in production mode. This may take a while!"
    INFILE="protein_ids.csv"
    OUTFILE="uniprot_results.csv"
fi

explain_read_write "${INFILE}" "${OUTFILE}"
prompt_if_exists "data/out/${OUTFILE}"

read -p "Press enter to continue (use 'Control+C' to exit) ... "

python ../../src/uniprot.py "data/in/${INFILE}" "data/out/${OUTFILE}"

echo "data has been downloaded"
echo "Generating fasta files suitable for upload to '?'"

if [ -d data/out/fasta ]; then 
    rm -r data/out/fasta     
fi

mkdir data/out/fasta

python ../../src/fasta.py "data/out/${OUTFILE}" "data/out/fasta"