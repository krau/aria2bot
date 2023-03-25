FROM python:3.11.2-alpine3.17

COPY . /aria2bot
WORKDIR /aria2bot
RUN pip install -r requirements.txt
ENTRYPOINT [ "python","/aria2bot/bot.py" ]