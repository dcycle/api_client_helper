#!/bin/bash
#
# Continuous integration script.
#
set -e

echo "=>"
echo "=> Linting shell"
echo "=>"
./scripts/lint-shell.sh
echo "=>"
echo "=> Linting python"
echo "=>"
./scripts/lint-python.sh
echo "=>"
echo "=> Building Docker"
echo "=>"
docker build -t local-dcycle-api-client-helper-image .
echo "=>"
echo "=> Running all test_*.py files"
echo "=>"
find . -name "test_*.py" -print0 | tr '\n' '\0' | xargs -0 -I '$' \
  ./scripts/run-file.sh "$"
echo "=>"
echo "=> Testing with dummy dummy"
echo "=>"
docker run --rm local-dcycle-api-client-helper-image dummy dummy
echo "=>"
echo "=> Testing with dummy dummy, pretty print"
echo "=>"
docker run --rm local-dcycle-api-client-helper-image dummy dummy | python -m json.tool
echo "=>"
echo "=> Testing with dummy multistep"
echo "=>"
docker run --rm local-dcycle-api-client-helper-image dummy multistep
echo "=>"
echo "=> Testing with dummy jsonpath_example"
echo "=>"
docker run --rm local-dcycle-api-client-helper-image \
  dummy jsonpath_example \
  --jsonpath='$.hello[?(@.valid=1)].response' \
  --jsondecode=1
echo "=>"
echo "=> All tests passing!"
echo "=>"
