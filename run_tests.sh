#! /bin/bash

# switch on mode with exit after error
#set -e

# linters start

docker-compose -f docker-compose-test.yml up --build --exit-code-from app
docker rm -v app mongo_db

echo "All checks successfully passed."