#!/usr/bin/env bash

set -euo pipefail

curl -X POST -H "Content-Type: application/json" -d @api-manager-export.json -H "Authorization: Basic YWRtaW46YWRtaW4xMjMh" http://localhost:8080/apiman/system/import/ 
