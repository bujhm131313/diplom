#!/usr/bin/env bash

set -euo pipefail

KEYCLOAK_RESPONSE=`curl -s -X POST http://localhost:8080/auth/realms/master/protocol/openid-connect/token  -H "Content-Type: application/x-www-form-urlencoded" -d 'username=admin' -d 'password=admin123!' -d 'grant_type=password' -d 'client_id=admin-cli'`

ACCESS_TOKEN=`echo "$KEYCLOAK_RESPONSE" | jq -r '.access_token'`

curl -v -X POST -H "Content-Type: application/json" -d @faceapi.json -H "Authorization: Bearer $ACCESS_TOKEN" http://localhost:8080/auth/admin/realms
