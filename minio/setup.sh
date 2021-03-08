#!/usr/bin/env bash

set -euo pipefail

docker run -p 9000:9000 -d --name minio -e MINIO_ACCESS_KEY=accessaccess -e MINIO_SECRET_KEY=secretsecret minio/minio server /data
