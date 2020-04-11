#!/usr/bin/env bash
docker build --tag=jurnalrisa .

docker run --rm -it -p 4000:8080 $(docker build -q .)
