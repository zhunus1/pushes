FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y libpq-dev \
  && apt-get install -y libzbar-dev \
  && apt-get install -y apt-utils \
  && apt-get install -y gettext \
  && apt-get install -y python-dev \
  && apt-get install -y gcc

# Updating pip to latest version
RUN pip install --upgrade pip

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY compose/start.sh /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

WORKDIR /app
