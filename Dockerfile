FROM python:3.11.3-alpine3.17

COPY . /aria2bot
WORKDIR /aria2bot
RUN pip install -r requirements.txt
ENTRYPOINT [ "python","bot.py" ]