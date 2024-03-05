#!/bin/bash
set -e

lint_only=0
full=1
quick=0
clean=0

while getopts ":lfqc" opt; do
    case "${opt}" in
        l ) lint_only=1;;
        f ) full=1;;
        q ) quick=1;;
        c ) clean=1;;
    esac
done

if [ "$clean" -eq 1 ]
then
    rm -rf spec
    rm -rf snippets
    rm -rf redoc
    rm -rf generated
   exit
fi

npx speccy lint --skip info-contact spec/openapi.yaml
if [ "$lint_only" -eq 1 ]
then
    exit
fi

mkdir -p snippets
mkdir -p generated/spec/images
npx speccy resolve -j spec/openapi.yaml -o speccy_openapi.yaml
mv speccy_openapi.yaml generated/spec/openapi.yaml

cp -a redoc/images/* generated/spec/images
cp -a redoc/index.html generated/spec/index.html
cp -a redoc/index.redocly generated/spec/index.redocly
cp -a redoc/.redocly.yaml generated/spec

if [ "$full" -eq 1 ]
then
    python3 scripts/generate_yaml_code_samples.py  --output "./generated/spec/openapi.yaml"
    if [ "$quick" -eq 0 ]
    then
        openapi-spec-validator generated/spec/openapi.yaml
    fi
fi
