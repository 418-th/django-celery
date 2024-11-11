FROM python:3.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/


RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libgnomecanvas2-dev \
    libreadline-dev \
    libbz2-dev \
    zlib1g-dev \
    liblzma-dev \
    libpq-dev \
    libxml2-dev \
    libxmlsec1-dev \
    git && \
    apt-get install -y --no-install-recommends \
    nodejs npm && \
    npm install -g gulp bower && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY package.json bower.json /app/
RUN npm install && bower install --allow-root

COPY . /app/

RUN pip freeze > new_requirements.txt
