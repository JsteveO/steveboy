#!/bin/bash

#exit early on errors
set -eu

#python buffers stdout.
export PYTHONNUNBUFFERED=true

python3 -m pip install -U pip

#install the requirements
python3 -m pip install -r requirements.txt

#run a glorious python3 server
python3 server.py
