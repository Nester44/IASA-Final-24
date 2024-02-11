FROM --platform=$BUILDPLATFORM python:3.10 AS builder

WORKDIR /app

ENV GECKODRIVER_VER v0.34.0
ENV FIREFOX_VER 100.0

RUN apt update
RUN apt upgrade -y
RUN apt install -y firefox-esr

RUN apt-get install -y locales
RUN locale-gen uk_UA
RUN dpkg-reconfigure locales

RUN apt install -y \
       libx11-xcb1 \
       libdbus-glib-1-2 \
   && curl -sSLO https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VER}/linux-x86_64/en-US/firefox-${FIREFOX_VER}.tar.bz2 \
   && tar -jxf firefox-* \
   && mv firefox /opt/ \
   && chmod 755 /opt/firefox \
   && chmod 755 /opt/firefox/firefox

RUN set -x \
   && curl -sSLO https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VER}/geckodriver-${GECKODRIVER_VER}-linux64.tar.gz \
   && tar zxf geckodriver-*.tar.gz \
   && mv geckodriver /usr/bin/

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
	pip3 install -r requirements.txt

COPY . /app