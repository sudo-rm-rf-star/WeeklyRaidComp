git pull
pip3 install -r requirements
python3 bot.py &>> logs/dokbot-$(date +%d-%m-%Y).log &
