FROM python:3.9

# create app directory
WORKDIR /usr/src/app

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .

# copy project
COPY . .

