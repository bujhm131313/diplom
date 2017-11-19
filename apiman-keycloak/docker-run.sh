#!/usr/bin/env bash

set -euo pipefail

docker run --name apiman --rm -d --network=host apiman/on-wildfly10
