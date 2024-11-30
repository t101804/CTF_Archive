FROM node:21

WORKDIR /usr/src/bot

COPY . /usr/src/bot
RUN apt-get update -y
RUN npm install

RUN npx playwright install-deps
RUN npx playwright install firefox


CMD ["node", "/usr/src/bot/bot.js"]