FROM arm32v6/node:9.3.0-alpine
RUN apk add --no-cache --virtual .build-deps \
        binutils-gold \
        g++ \
        gcc \
        gnupg \
        libgcc \
        linux-headers \
        make \
        python
RUN wget abyz.co.uk/rpi/pigpio/pigpio.zip && unzip pigpio.zip && cd PIGPIO && make -i -k && make -i -k install
WORKDIR /app
ADD index.js .
ADD package.json .
RUN npm install
RUN apk del .build-deps
CMD [ "node", "index.js" ]
