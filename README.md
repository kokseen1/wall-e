# Garbage Collector Bot


## Prerequisites

Ensure that you have [docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) installed on your machine.

## Installation

Clone the repository

```
git clone https://github.com/kokseen1/garbage-collector-bot.git
```
## Deployment

### Local

Create a `.env` file

```
cd garbage-collector-bot
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

Run `sudo docker-compose up`

<!-- ### On Heroku -->
