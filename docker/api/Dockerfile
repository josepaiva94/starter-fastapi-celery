FROM python:3-alpine

LABEL maintainer="José Carlos Paiva <josepaiva94@gmail.com>"
LABEL description="Docker container w/ the API."

COPY pyproject.toml .

RUN apk update && \
    apk add gcc libc-dev libffi-dev openssl-dev python3-dev && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry install

EXPOSE 8000
