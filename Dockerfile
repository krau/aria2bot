FROM python:3.11.6-slim-bookworm

COPY . /aria2bot
WORKDIR /aria2bot
RUN pip install -r requirements.txt
ENTRYPOINT [ "python","bot.py" ]