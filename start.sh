#!/bin/bash
app="docker.test"
docker build --platform linux/amd64 -t ${app} .
docker run --platform linux/amd64 -d -p 56733:80 \
  --name=${app} \
  -v $PWD:/app ${app}