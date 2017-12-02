#!/usr/bin/env bash
# Remember to install jq (e.g. brew install jq; yum install jq; apt-get install jq)

set -e
RED='\033[0;31m'
NORMAL='\033[0m'

printf "${RED}Getting OAuth2 token from Keycloak (includes access_token, refresh_token, etc):${NORMAL}\n"
KEYCLOAK_RESPONSE=`curl -s -X POST http://127.0.0.1:8080/auth/realms/faceapi/protocol/openid-connect/token  -H "Content-Type: application/x-www-form-urlencoded" -d 'username=faceapiuser' -d 'password=faceapiuser' -d 'grant_type=password' -d 'client_id=apiman'`
printf "$KEYCLOAK_RESPONSE \n\n"

printf "${RED}Parsing access_token field, as we don't need the other elements:${NORMAL}\n"
ACCESS_TOKEN=`echo "$KEYCLOAK_RESPONSE" | jq -r '.access_token'`
printf "$ACCESS_TOKEN \n\n"

printf "${RED}Accessing service via apiman using token - we will put it into the Authorization header:${NORMAL}\n"
curl -k -v -H "Authorization: Bearer $ACCESS_TOKEN" https://localhost:8443/apiman-gateway/FaceAPI/faceapi/v1
printf "\n\n"
