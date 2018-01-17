FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /code
WORKDIR /code
ADD requirements.txt /code/
ADD requirements.example.txt /code/
RUN pip install -U pip
RUN pip install -r requirements.txt && pip install -r requirements.example.txt
ADD . /code/


