#!/bin/bash

set -e

usage() {
    echo "usage: quick_clean_dirs.sh LOG_DIR_NAME"
    exit 1
}

case "$#" in
    "1")
        fn=$1
        ;;
    *)
        usage
        ;;
esac

if [ "${fn::5}" = "logs/" ]; then
    fn="${fn:5}"
fi

if ! [ -d "ALF_data/_$fn" ]; then
    mkdir "ALF_data/_$fn"
    echo "made directory ALF_data/_$fn"
fi

for d in $(ls "logs/$fn" | grep "\.log$"); do
    ./cleanup_dirs.sh "logs/$fn/$d" "ALF_data/_$fn"
done
