#!/bin/sh

# you should have python3 installed

# make sure that you have set permissions for this file:
# chmod 755 init.sh

# to run this script use the following
# source ./init.sh

# use 'deactivate' to disable the environment

if [ -d env ]; then 
    source env/bin/activate
else    
    python3 -m venv env
    source env/bin/activate
    if [ "$(pwd)/env/bin/python" = "$(which python)" ]; then 
        echo "python environment set"
        pip install --upgrade pip
        pip install -r requirements.txt
    else
        echo "something went wrong when setting the python environment"
        exit 1
    fi
fi

# python -m pip --version
