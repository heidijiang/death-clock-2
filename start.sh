#!/bin/bash
app="docker.test"
docker build --platform linux/amd64 -t ${app} .
docker run --platform linux/amd64 -d -p 5000:5000 ${app}