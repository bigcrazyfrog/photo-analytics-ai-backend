FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

WORKDIR /code

COPY . /code

RUN apt-get update && \
    python -m pip install --upgrade pip && \
    pip install -r requirements/local_build.txt

RUN inv project.init
