# Garbage Collector Bot

## Prerequisites

Ensure that you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed on your machine.

### Deploying on Heroku

- Ensure that you have [Heroku](https://devcenter.heroku.com/articles/heroku-cli) installed on your machine.
- Ensure that you have [psql](https://www.postgresql.org/download/) on your machine.

## Installation

Clone the repository

```shell
git clone https://github.com/kokseen1/garbage-collector-bot.git
cd garbage-collector-bot
```

## Deployment

### Local

Create a `.env` file

```shell
touch .env
```

Set environment variables by adding these lines in `.env` (modify as required)

```
BOT_TOKEN=<Telegram bot token>
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
NO_SSL_VERIFY=True
```

Build and start the containers

```shell
sudo docker-compose up
```

### Heroku

Login to Heroku

```shell
heroku login
```

Create a Heroku app and add the Git remote

```shell
heroku create -a <Heroku app name>
heroku git:remote -a <Heroku app name>
```

Set the stack of your app to `container`

```shell
heroku stack:set container
```

Add the `postgresql` addon

```shell
heroku addons:create heroku-postgresql:hobby-dev
```

Set the environment variables

```shell
heroku config:set HEROKU_URL=https://<Heroku app name>.herokuapp.com/
heroku config:set BOT_TOKEN=<Telegram bot token>
heroku config:set POSTGRES_NAME=postgres
heroku config:set POSTGRES_USER=postgres
heroku config:set POSTGRES_PASSWORD=postgres
```

Connect to the database

```shell
heroku pg:psql
```

Create tables

```sql
CREATE TABLE sent (
	item_id VARCHAR ( 255 ) NOT NULL,
	chat_id VARCHAR ( 255 ) NOT NULL
);

CREATE TABLE queries (
	query_text VARCHAR ( 255 ) NOT NULL,
	chat_id VARCHAR ( 255 ) NOT NULL
);
```

Push to Heroku

```shell
git push heroku main
```
