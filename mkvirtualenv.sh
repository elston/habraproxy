#!/bin/bash
text="venv"
if [[ $1 != '' ]]; then
    text=$1
fi
virtualenv $text