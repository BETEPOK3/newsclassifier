FROM python:3.8
ARG path=services/web

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code
ADD schema ./schema

WORKDIR ./$path
COPY ./$path/requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000