#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "usage: $0 INSTANCE" 1>&2
    exit 1
else
    for pid in $(pgrep -f "ALF-master$1"); do
        kill $pid
        echo "killed $pid"
    done
fi
