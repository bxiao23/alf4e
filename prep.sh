#!/bin/bash

case "$1" in
    "r"*)
        PYALF_HOME="/home/bxiao23/alf/pyALF-master"
        tag=${1:1}
        # for compatibility; might change someday
        if [ "$tag" == "1" ]; then
            ALF_HOME="/home/bxiao23/alf/ALF-master"
        else
            ALF_HOME="/home/bxiao23/alf/ALF-master${tag}"
        fi
        ;;
    *)
        ALF_HOME="/home/ganzfeld/fourelectron/alf/ALF-master"
        PYALF_HOME="/home/ganzfeld/fourelectron/alf/pyALF-master"
        ;;
esac

if [[ "${PYTHONPATH-}" != *"$PYALF_HOME"* ]]; then
    export PYTHONPATH="$PYALF_HOME:$PYTHONPATH"
fi
export ALF_DIR="$ALF_HOME"
