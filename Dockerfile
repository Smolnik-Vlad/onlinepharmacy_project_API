FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

ADD . /app/

RUN pip install --upgrade pip && \
    pip install -r requirements.txt