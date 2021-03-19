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
./scripts/run-all-test-files.sh
echo "=>"
echo "=> Testing with dummy dummy, do not pretty print with"
echo "=> '| python -m json.tool' because python may not always be installed"
echo "=>"
docker run --rm local-dcycle-api-client-helper-image dummy dummy
echo "=>"
echo "=> Testing with dummy multistep"
echo "=>"
docker run --rm \
  --env DEBUG=1 \
  -v "$(pwd)":/usr/src/app \
  local-dcycle-api-client-helper-image dummy multistep
echo "=>"
echo "=> Testing with dummy jsonpath_example"
echo "=>"
docker run --rm \
  -v "$(pwd)":/usr/src/app \
  local-dcycle-api-client-helper-image \
  dummy jsonpath_example \
  --jsonpath='$.hello[?(@.valid=1)].response' \
  --jsondecodefirst=1
echo "=>"
echo "=> Testing with dummy mock_list"
echo "=>"
docker run --rm dcycle/api_client_helper:1 dummy mock_list
echo "=>"
echo "=> Testing with dummy mock_delete"
echo "=>"
docker run --rm \
  --env ID="456" \
  dcycle/api_client_helper:1 dummy mock_delete
NAME=hello
echo "=>"
echo "=> Testing with dummy mock_delete_all_by_name"
echo "=>"
docker run --rm \
  --env NAME="$NAME" \
  dcycle/api_client_helper:1 dummy mock_delete_all_by_name
echo "=>"
echo "=> All tests passing!"
echo "=>"
