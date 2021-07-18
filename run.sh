#!/bin/bash
CUR_DIR=$(pwd)
cd "$(dirname "$0")"
git pull
git checkout frontend
git reset --hard origin/frontend
docker-compose build
docker-compose up -d
cd $CUR_DIR
