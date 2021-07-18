FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY *.py /
COPY *.json /
COPY *.js /
COPY ["src/", "src/"]
COPY ["static/", "static/"]

ENTRYPOINT ["python3", "bot.py", "&>> logs/dokbot-$(date +%d-%m-%Y).log &"]