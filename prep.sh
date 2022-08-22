#!/bin/bash

case "$1" in
    "r"|"roch"|"r1"|"roch1")
        ALF_HOME="/home/bxiao23/alf/ALF-master"
        PYALF_HOME="/home/bxiao23/alf/pyALF-master"
        ;;
    "r2"|"roch2")
        ALF_HOME="/home/bxiao23/alf/ALF-master2"
        PYALF_HOME="/home/bxiao23/alf/pyALF-master"
        ;;
    "r3"|"roch3")
        ALF_HOME="/home/bxiao23/alf/ALF-master3"
        PYALF_HOME="/home/bxiao23/alf/pyALF-master"
        ;;
    "r4"|"roch4")
        ALF_HOME="/home/bxiao23/alf/ALF-master4"
        PYALF_HOME="/home/bxiao23/alf/pyALF-master"
        ;;
    "r5"|"roch5")
        ALF_HOME="/home/bxiao23/alf/ALF-master5"
        PYALF_HOME="/home/bxiao23/alf/pyALF-master"
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
