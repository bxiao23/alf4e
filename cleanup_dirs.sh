#!/bin/bash

set -e

usage() {
    echo "usage: cleanup_dirs.sh LOG_FN DEST" 1>&2
    exit 1
}

case "$#" in
    "2")
        fn=$1
        dest=$2
        ;;
    *)
        usage
        ;;
esac

if ! [ -f "$fn" ]; then
    if [ -f "logs/$fn" ]; then
        fn="logs/$fn"
    else if [ -f "logs/$fn.log" ]; then
        fn="logs/$fn.log"
    else if [ -f "$fn.log" ]; then
        fn="$fn.log"
    fi; fi; fi
fi
echo "file: $fn"

n=$(grep -e 'total number of runs' $fn | grep -oe '[[:digit:]]*')

gen_dirs=$(grep -A$n -e 'list of generated directories' $fn | tail -n +2)

for dir in $gen_dirs; do
    mv -i $dir $dest
done
