FROM python:3.10-alpine

ENV PYTHONBUFFERED=1

WORKDIR /app

COPY . .

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt 

EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]