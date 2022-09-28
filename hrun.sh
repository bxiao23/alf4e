#!/bin/bash

MAX_ALF=13

usage() {
    echo "Usage: $0 [-a N_AUTOCORR_BINS] [-o OBS_DIR] [-L LOG_DIR] [ -l LOG_NAME] -d RESULT_DIR -c CONFIG" 1>&2
    exit 1
}

AUTOCORR_BINS=""
OBS_DIR="obs/"
LOG_DIR="logs/"

while getopts ":a:o:L:d:l:c:" arg; do
    case "$arg" in
        "a")
            AUTOCORR_BINS=${OPTARG}
            ;;
        "o")
            OBS_DIR=${OPTARG}
            if [ "${OBS_DIR: -1}" != '/' ]; then
                OBS_DIR="$OBS_DIR/"
            fi
            ;;
        "L")
            LOG_DIR=${OPTARG}
            if [ "${LOG_DIR: -1}" != '/' ]; then
                OBS_DIR="$LOG_DIR/"
            fi
            ;;
        "d")
            RESULT_DIR=${OPTARG}
            if [ "${RESULT_DIR: -1}" = '/' ]; then
                RESULT_DIR=${RESULT_DIR::-1}
            fi
            ;;
        "l")
            LOG_NAME=${OPTARG}
            ;;
        "c")
            CONFIG=${OPTARG}
            ;;
        ":")
            echo "flag requires a parameter" 1>&2
            usage
            ;;
        "/?")
            echo "flag not recognized" 1>&2
            usage
            ;;
    esac
done

if [ -z "${RESULT_DIR+x}" ] || [ -z "${CONFIG+x}" ]; then
    usage
fi

if [ -z "${LOG_NAME+x}" ]; then
    # by default, log name is same as config name
    LOG_NAME=$(basename "$CONFIG" '.yaml').log
fi

if [[ "$RESULT_DIR" == "$OBS_DIR"* ]]; then
    RESULT_DIR=${RESULT_DIR:${#OBS_DIR}}
    echo "truncated RESULT_DIR to $RESULT_DIR"
else if [[ "$RESULT_DIR" == "$LOG_DIR"* ]]; then
    RESULT_DIR=${RESULT_DIR:${#LOG_DIR}}
    echo "truncated RESULT_DIR to $RESULT_DIR"
fi; fi
OBS_DIR=$OBS_DIR$RESULT_DIR
LOG_DIR=$LOG_DIR$RESULT_DIR

for inst in $(seq 1 $MAX_ALF) 'END'; do
    if [ -z "$(pgrep -f ALF-master$inst)" ]; then
        break
    fi
done
if [ "$inst" == 'END' ]; then
    echo "no available ALF instances"
    exit 2
fi
source prep.sh "r$inst"
echo "selected ALF-master$inst"

if [ -n "$AUTOCORR_BINS" ] && ! [[ "${OBS_DIR}" == *"autocorr" ]]; then
    OBS_DIR="${OBS_DIR}_autocorr"
fi
if ! [ -d "$OBS_DIR" ]; then
    echo "creating $OBS_DIR"
    mkdir $OBS_DIR
fi
if ! [ -d "$LOG_DIR" ]; then
    echo "creating $LOG_DIR"
    mkdir $LOG_DIR
fi

if [ -n "$AUTOCORR_BINS" ]; then
    nohup python -u hubbard_4spin.py --obs_prefix "$OBS_DIR" "$CONFIG" \
            --run_autocorr_trial "$AUTOCORR_BINS" &>"$LOG_DIR/$LOG_NAME" &
    echo $!
else
    nohup python -u hubbard_4spin.py --obs_prefix "$OBS_DIR" "$CONFIG" &>"$LOG_DIR/$LOG_NAME" &
    echo $!
fi
