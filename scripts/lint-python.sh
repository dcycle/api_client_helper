#!/bin/bash
#
# Lint python scripts.
#
set -e

find . -name "*.py" -print0 | tr '\n' '\0' | xargs -0 -I '$' docker run --rm -v "$(pwd)":/app/code dcycle/python-lint:1 /app/code/"$"
