FROM alpine:3.7

WORKDIR /usr/src/app
COPY . .
RUN apk add --no-cache python3 \
    && python3 -m pip install -r requirements.txt \
    && python3 -m pip install --upgrade pip \
    && python3 nagios-scraper.py
