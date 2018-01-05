FROM arm32v6/node:9.3.0-alpine

WORKDIR /app
ADD index.js .
ADD package.json .
RUN npm install
CMD [ "node", "index.js" ]
