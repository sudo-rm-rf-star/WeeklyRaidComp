git pull
pip install -r requirements
python bot.py &>> logs/dokbot-$(date +%d-%m-%Y).log &
