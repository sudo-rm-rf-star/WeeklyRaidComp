#!/bin/bash
CUR_DIR=$(pwd)
cd "$(dirname "$0")"
git pull
git checkout production
git reset --hard origin/production
python3 -m pip install -r requirements.txt
mkdir -p logs
python3 bot.py &>> logs/dokbot-$(date +%d-%m-%Y).log &
cd $CUR_DIR
