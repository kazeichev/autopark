#!/usr/bin/env bash

docker build - < Dockerfile # build project
docker-compose up -d # up project

cat dump.sql | docker exec -i postgis psql -U postgres # restore tables