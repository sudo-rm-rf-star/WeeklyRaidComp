#!/bin/bash
CUR_DIR=$(pwd)
cd "$(dirname "$0")"
git pull
git checkout production
git reset --hard origin/production
docker-compose build
docker-compose up -d
cd $CUR_DIR
