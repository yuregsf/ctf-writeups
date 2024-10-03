FROM node:13.14.0-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

COPY flag.txt /app/flag.txt

EXPOSE 3000

CMD ["node", "server.js"]