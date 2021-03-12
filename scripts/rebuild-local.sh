#!/bin/bash
# Rebuild locally.
# This can be used during local development if needed.

set -e

PROJECT=api_client_helper
MAJORVERSION='1'

docker build -t dcycle/"$PROJECT:$MAJORVERSION" .
