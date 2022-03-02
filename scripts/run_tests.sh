#!/usr/bin/env bash

# stop current script if any error happens
set -e

# get parent folder
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )";
PARENT_DIRECTORY="${DIR%/*}"

# go to parent folder
cd ${PARENT_DIRECTORY}

# run all unit tests
python -m pytest --import-mode=append tests/
# python -m unittest discover