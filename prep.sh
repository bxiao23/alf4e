#!/bin/bash

ALF_HOME="/home/bxiao23/alf/ALF-master"
PYALF_HOME="/home/ganzfeld/fourelectron/alf/pyALF-master"

if [[ "${PYTHONPATH-}" != *"$PYALF_HOME"* ]]; then
    export PYTHONPATH="$PYALF_HOME:$PYTHONPATH"
fi
export ALF_DIR="$ALF_HOME"
