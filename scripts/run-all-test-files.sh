#!/bin/bash
#
# Run a single python file on Docker.
#
set -e

find . -name "test_*.py" -print0 | tr '\n' '\0' | xargs -0 -I '$' \
  ./scripts/run-file.sh "$"
