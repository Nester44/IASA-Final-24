FROM node:18

WORKDIR /srv/app/

ENV PATH /srv/app/node_modules/.bin:$PATH

COPY package.json ./
COPY package-lock.json ./
RUN npm i

COPY . ./