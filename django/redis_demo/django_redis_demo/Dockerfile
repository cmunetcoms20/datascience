FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get update -y && apt-get install whois
RUN mkdir /code
WORKDIR /code
COPY django/redis_demo/django_redis_demo/ /code/
RUN pip install -r requirements.txt
RUN echo $REDIS_PORT
RUN echo $REDIS_HOST
