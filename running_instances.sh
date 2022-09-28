#!/bin/bash

pgrep -af 'ALF-master' | grep -o 'ALF-master.*/' | grep -o '[[:digit:]]*' | sort -n | tr "\n" " "
echo ""
