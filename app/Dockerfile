FROM python:3.8-slim-buster

LABEL name="BoneBolts" maintainer="Nino Lopez<ninolopez91@gmail.com>"

ARG APP_ROOT=/usr/src/app/

# set work directory
WORKDIR ${APP_ROOT}

USER root
# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update

RUN apt-get install -y gcc libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev

COPY Pipfile* ${APP_ROOT}/

RUN pip install --upgrade pip \
    && pip install pipenv \
    && pipenv install --dev --system --python=`which python3` \
    && chown -R 1001:0 ${APP_ROOT} \
    && chmod -R +w ${APP_ROOT}


USER 1001

COPY . ${APP_ROOT}

EXPOSE 8080
