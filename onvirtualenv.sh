#!/bin/bash
text="venv"
if [[ $1 != '' ]]; then
    text=$1
fi
# . $text/bin/activate
# source $text/bin/activate
source venv/bin/activate
