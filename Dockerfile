FROM resin/rpi-raspbian:stretch

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python \
    wget \
    python-dev \
    python-virtualenv \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://bootstrap.pypa.io/get-pip.py && python get-pip.py

WORKDIR /app

COPY . .

RUN pip install setuptools

RUN pip install -r requirements.txt

CMD [ "python", "/app/main.py" ]

EXPOSE 8080
