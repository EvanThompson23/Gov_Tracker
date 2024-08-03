FROM python:3.10 AS build

WORKDIR /Gov_Tracker

COPY . /Gov_Tracker

RUN pip install --trusted-host pypi.python.org -r requirements.txt

#  apt-get update && apt-get install -y wget unzip && \
#    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
#    apt install -y ./google-chrome-stable_current_amd64.deb && \
#    rm google-chrome-stable_current_amd64.deb && \
#    apt-get clean
