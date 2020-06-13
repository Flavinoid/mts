
function ensure_exists () {
    if [ ! -f "${1}" ]; then
        printf "It looks like the file '%s' does not exist\ntry using the `run.sh` script instead" "${1}"
        exit 1
    fi
}

if [ "${1}" = "--dev" ]; then     
    INFILE="uniprot_results_sample.csv"
else    
    INFILE="uniprot_results.csv"
fi

ensure_exists "data/out/${INFILE}"

if [ -d data/out/fasta ]; then 
    echo "it looks like '/data/out/fasta' already exists"
    echo "are you sure you want to overwrite it"
    read -p "Press enter to continue (use 'Control+C' to exit) ... "
    rm -r data/out/fasta     
fi

mkdir data/out/fasta

python ../../src/fasta.py "data/out/${INFILE}" "data/out/fasta"