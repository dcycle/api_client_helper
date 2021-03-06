#!/bin/bash
#
# Run a single python file on Docker.
#
set -e

echo "=>"
echo "=> Running $1"
echo "=>"
docker run -v "$(pwd)":/usr/src/app --rm --entrypoint python3 \
local-dcycle-api-client-helper-image "$1"
