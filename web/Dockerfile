FROM python:3.5.4-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /project/addons/django-notifications
ADD django-notifications .
WORKDIR /project/addons/python-graph
ADD python-graph .
WORKDIR /project/addons
ADD ./requirements.txt .

RUN  apk update && apk add postgresql-dev gcc python3-dev musl-dev && apk add jpeg-dev zlib-dev && pip install -r requirements.txt && cd django-notifications && pip install . && cd ../python-graph/core/ && pip install . && cd ../dot/ && pip install .
 
WORKDIR /project/code



 
