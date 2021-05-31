FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev gcc  -y
WORKDIR /django
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

