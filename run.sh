#!/usr/bin/env bash
set -ex

[ ! -d $PWD/venv ] && virtualenv3 --system-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
pip install .
wluma-als-emulator -o $(mktemp -d) -v $@
