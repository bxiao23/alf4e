#!/bin/bash

if [ "$#" -eq 1 ]; then
    ln -s "$1/data.h5" "Analysis/data.h5"
    ln -s "$1/parameters" "Analysis/parameters"
else
    echo "usage: setup_analysis.sh ALF_RUN_DATA_DIR" 1>&2
    exit 1
fi
