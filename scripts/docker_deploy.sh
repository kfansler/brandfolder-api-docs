#!/bin/bash

docker cp spec $(docker ps | grep openapi | awk '{print $1}'):openapi
docker cp snippets $(docker ps | grep openapi | awk '{print $1}'):openapi
docker cp redoc $(docker ps | grep openapi | awk '{print $1}'):openapi
docker exec $(docker ps | grep openapi | awk '{print $1}') scripts/build.sh $@
if [ $? -eq 0 ]
then
    echo View Smartsheet API documentation here: http://localhost:${REDOC_PORT:-8000}
else
    echo Specification has errors
    exit 1
fi
