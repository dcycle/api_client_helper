#!/bin/bash
#
# Continuous integration script.
#
set -e

./scripts/lint-shell.sh
./scripts/lint-python.sh

docker build -t local-dcycle-api-client-helper-image .

find . -name "test_*.py" -print0 | tr '\n' '\0' | xargs -0 -I '$' \
  docker run --rm --entrypoint python3 \
  local-dcycle-api-client-helper-image "$"

docker run --rm local-dcycle-api-client-helper-image dummy dummy
docker run --rm local-dcycle-api-client-helper-image dummy dummy | python -m json.tool
docker run --rm local-dcycle-api-client-helper-image dummy multistep
docker run --rm local-dcycle-api-client-helper-image \
  dummy jsonpath_example \
  --jsonpath='$.hello[?(@.valid=1)].response' \
  --jsondecode=1
