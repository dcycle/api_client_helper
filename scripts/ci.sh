#!/bin/bash
#
# Continuous integration script.
#
set -e

./scripts/lint-shell.sh
./scripts/lint-python.sh
