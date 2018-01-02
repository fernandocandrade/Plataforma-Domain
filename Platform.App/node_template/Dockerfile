FROM node:carbon

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 9090

RUN chmod +x /usr/src/app/executeApp.sh

CMD [ "/usr/src/app/executeApp.sh" ]