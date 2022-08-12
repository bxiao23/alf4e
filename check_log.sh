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

# as of now intended for two formats:
#   t=t U=U mu=mu dt=dtau b=beta phi=phi  (new format; total of 9 fields)
#   t=t U=U dt=dtau b=beta                (old format; total of 7 fields)
prog='{if (NF == 9) {print $3"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8} else {print $3"\t"$4"\t"$5"\t"$6}}'

done=$(grep -e 'STARTING' "$fn" | awk "$prog")
if [ -z "${count_only-}" ]; then
    echo "$done"
fi
#last_chem=$(grep -Eoe 'chem=-?[[:digit:]]*\.[[:digit:]]*' "$fn" | tail -1)
#last_chem=${last_chem:5}
#echo "last mu: $last_chem"
echo "completed runs: "$(( $(echo "$done" | wc -l) - 1 ))
