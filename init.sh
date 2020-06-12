if [ -d env ]; then 
    source env/bin/activate
else
    python3 -m venv env
    source env/bin/activate
fi