FROM python:3.8
ARG path=services/classifier

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR code/$path
COPY ./$path/requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8001