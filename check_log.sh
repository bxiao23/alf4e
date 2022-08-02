#!/bin/bash

fn="logs/alf.log"


if [ "$#" -eq 1 ]; then
    if [ "$1" == "-c" ]; then
        count_only=1
    else
        fn="$1"
    fi
else if [ "$#" -eq 2 ]; then
    if [ "$1" != "-c" ]; then
        echo "usage: check_logs.sh [-c] [FILENAME]" 1>&2
        exit 1
    else
        count_only=1
        fn="$2"
    fi
fi; fi

if [ "${fn:0:1}" == "-" ]; then
    echo "filename cannot start with hyphen" 1>&2
    exit 1
fi

done=$(grep -e 'STARTING' "$fn" | awk '{print $3"\t"$4"\t"$5"\t"$6}')
if [ -z "${count_only-}" ]; then
    echo "$done"
fi
echo "completed "$(echo "$done" | wc -l)
