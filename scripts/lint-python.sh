#!/bin/bash
#
# Lint python scripts.
#
set -e

echo "Linting Python"
echo "To ignore a warning, place a comment before the offending line:"
echo ""
echo "# pylint: disable=E0401"
echo "..."
echo ""

find . -name "*.py" -print0 | tr '\n' '\0' | xargs -0 -I '$' docker run --rm -v "$(pwd)":/app/code dcycle/python-lint:1 /app/code/"$"
