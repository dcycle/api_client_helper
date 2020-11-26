#!/bin/bash
#
# Lint shell scripts.
#
set -e

find . -name "*.sh" -print0 | \
  xargs -0 docker run --rm -v "$(pwd)":/code dcycle/shell-lint
