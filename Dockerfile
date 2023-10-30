FROM python:3.11

RUN mkdir /sn_app

WORKDIR /sn_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .