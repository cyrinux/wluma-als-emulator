#!/usr/bin/env bash
set -ex

[ ! -d $PWD/venv ] && python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install .
wluma-als-emulator -o $(mktemp -d) -v $@
