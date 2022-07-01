# WALL-E

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- An available [Telegram Bot](https://t.me/botfather/)

### Deploying on Heroku

- [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
- [psql](https://www.postgresql.org/download/)

## Installation

Clone this repository

```shell
git clone https://github.com/kokseen1/wall-e.git
cd wall-e
```

## Local Deployment

Create a `.env` file

```shell
touch .env
```

Set environment variables by adding the following lines in `.env`

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

## Heroku Deployment

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

Add the Heroku `postgresql` addon

```shell
heroku addons:create heroku-postgresql:hobby-dev
```

Set environment variables

```shell
heroku config:set HEROKU_URL=https://<Heroku app name>.herokuapp.com/
heroku config:set BOT_TOKEN=<Telegram bot token>
heroku config:set POSTGRES_NAME=postgres
heroku config:set POSTGRES_USER=postgres
heroku config:set POSTGRES_PASSWORD=postgres
```

Connect to the database via `psql`

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

Exit from `psql`
```shell
exit
```

Push to Heroku

```shell
git push heroku main
```

Keep the application awake via a service like [Kaffeine](https://kaffeine.herokuapp.com/)

## Bot Usage

Add query

```
/add <query>
```

Remove query

```
/rm <query>
```

List queries

```
/ls
```

Fetch queries

```
/force
```
