FROM python:3.9-alpine
RUN apk add --no-cache build-base
WORKDIR /app
COPY main.py requirements.txt ./
RUN CFLAGS=-fcommon pip install --no-cache-dir -r requirements.txt
RUN apk del build-base
EXPOSE 8080
ENV PYTHONUNBUFFERED=0
CMD [ "python", "/app/main.py" ]