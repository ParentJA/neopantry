FROM python:3.6

ENV PYTHONUNBUFFERED 1

ADD ./requirements requirements
RUN pip install --upgrade pip
RUN pip install -r requirements/local.txt

WORKDIR /usr/src/app/neopantry
