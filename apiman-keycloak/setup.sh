#!/usr/bin/env bash

set -euo pipefail

URL=http://localhost:8080/auth

echo "Start Docker container"
./docker-run.sh
echo "Container started!"

echo "Waiting for Keycloak"
until $(curl --output /dev/null --silent --head --fail $URL); do
  printf '.'
  sleep 1
done
echo "Keycloak started!"

echo "Import Keycloak realm"
./keycloak-import.sh
echo "Keycloak realm imported!"

echo "Import Apiman API"
./apiman-import.sh
echo "Apiman API imported"
