FROM python:latest

RUN mkdir /src
WORKDIR /src
COPY . /src
ENV TZ Asia/Tashkent
RUN pip install -r requirements.txt