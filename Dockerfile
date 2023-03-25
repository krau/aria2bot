FROM python3.11

COPY . /aria2bot
WORKDIR /aria2bot
RUN pip install -r requirements.txt
CMD ["python3", "aria2bot"]
