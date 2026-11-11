FROM python:3.14.7-alpine

ARG USER_ID=1000
ARG GROUP_ID=1000
ARG USERNAME=appuser

RUN apk add --no-cache shadow

RUN addgroup -g $GROUP_ID $USERNAME \
    && adduser -u $USER_ID -G $USERNAME -s /bin/sh -D $USERNAME

RUN mkdir -p /app

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R $USERNAME:$USERNAME /app

USER $USERNAME 

LABEL maintainer="Pooya Danandeh"\
      description="My Website Project Running on Alpine Linux Image"

EXPOSE 8000