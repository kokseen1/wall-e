import os
import psycopg2
from telegram.ext import Updater, CommandHandler
from threading import Thread
import telegram

from api import api_search, LISTING_URL
from etc import randsleep

connection = None
cursor = None
bot = None


def get_message_data(update):
    """
    Parse Telegram `update` object and return chat ID and query text
    """
    message_json = update.message
    chat_id = str(message_json["chat"]["id"])
    message_full = message_json["text"]
    query_text = " ".join(message_full.split()[1:])

    return chat_id, query_text


def add(update, context):
    """
    Add a query for user
    """
    chat_id, query_text = get_message_data(update)
    if not query_text:
        return

    cursor.execute(
        f"INSERT INTO queries (query_text, chat_id) SELECT '{query_text}', '{chat_id}' WHERE NOT EXISTS (SELECT query_text FROM queries WHERE query_text='{query_text}' AND chat_id='{chat_id}');")
    connection.commit()


def remove(update, context):
    """
    Remove queries for user
    """
    chat_id, query_text = get_message_data(update)
    if not query_text:
        return

    if query_text == "*":
        # Delete all queries for user
        cursor.execute(f"DELETE FROM queries WHERE chat_id='{chat_id}';")
    else:
        # Delete a specific query for user
        cursor.execute(
            f"DELETE FROM queries WHERE query_text='{query_text}' AND chat_id='{chat_id}';")
    connection.commit()


def ls(update, context):
    """
    List all queries for user
    """
    chat_id, _ = get_message_data(update)
    cursor.execute(f"SELECT * FROM queries WHERE chat_id='{chat_id}';")
    record = cursor.fetchall()
    query_list = [item[0] for item in record]
    if not query_list:
        return

    queries_string = "\n".join(query_list)
    update.message.reply_text(queries_string)


def force(update, context):
    """
    Force fetch all queries for user
    """
    chat_id, _ = get_message_data(update)
    cursor.execute(f"SELECT * FROM queries WHERE chat_id='{chat_id}';")
    record = cursor.fetchall()

    for query_text, chat_id in record:
        search_and_notify(query_text, chat_id)

        # Sleep after each query
        randsleep(1, 10)


def search_and_notify(query_text, chat_id):
    """
    Performs an api request and notifies the user of the results
    """
    resp = api_search(query_text)
    if not resp:
        # Invalid request
        return

    # Garbage filter to be improved
    # filter_bubbles = resp["data"].get("filterBubbles")
    # if filter_bubbles and "InstantBuy" in str(filter_bubbles):
    #     # Ignore garbage response
    #     print("Ignored garbage")
    #     return

    # Handle search results
    for _, result in enumerate(resp["data"]["results"]):
        listingCard = result["listingCard"]
        item_id = listingCard["id"]
        title = listingCard["title"]

        # Fetch sent listings from database
        cursor.execute(f"SELECT * FROM sent;")
        record = cursor.fetchall()

        print(f"[SAVED_IDS] {len(record)} items")

        already_sent = (item_id, chat_id) in record
        if already_sent:
            # Skip sent listings
            continue

        try:
            # Send message to the user
            bot.sendMessage(chat_id, f"{title}\n{LISTING_URL.format(item_id)}")
        except Exception as e:
            print(f"[TELEGRAM EXCEPTION] {e}")
            # continue

        # Update the sent database with listing
        cursor.execute(
            f"INSERT INTO sent (item_id, chat_id) SELECT '{item_id}', '{chat_id}' WHERE NOT EXISTS (SELECT item_id FROM sent WHERE item_id='{item_id}' AND chat_id='{chat_id}');")
        connection.commit()


def main_loop():
    """
    Main loop to poll and notify users
    """
    while True:
        # Retrieve all queries from database
        cursor.execute(f"SELECT * FROM queries;")
        record = cursor.fetchall()

        # Handle every query
        for query_text, chat_id in record:
            search_and_notify(query_text, chat_id)

            # Sleep after each query
            randsleep(1, 10)

        # Sleep after each cycle
        randsleep(600, 1000)


def main():
    """
    Main Telegram bot listener
    """
    # Retrieve environment variables
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    HEROKU_URL = os.environ.get("HEROKU_URL")

    # Initialize Telegram bot
    global bot
    if not bot:
        bot = telegram.Bot(BOT_TOKEN)

    # Connect to the database
    global connection, cursor
    if not connection:
        if HEROKU_URL:
            DATABASE_URL = os.environ.get("DATABASE_URL")
            connection = psycopg2.connect(DATABASE_URL)
        else:
            POSTGRES_NAME = os.environ.get("POSTGRES_NAME")
            POSTGRES_USER = os.environ.get("POSTGRES_USER")
            POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
            POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
            connection = psycopg2.connect(
                database=POSTGRES_NAME, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST)

    if not cursor:
        cursor = connection.cursor()

    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Add command handlers
    updater.dispatcher.add_handler(CommandHandler("add", add))
    updater.dispatcher.add_handler(CommandHandler("rm", remove))
    updater.dispatcher.add_handler(CommandHandler("ls", ls))
    updater.dispatcher.add_handler(CommandHandler("force", force))

    # Start the api polling loop in a thread
    Thread(target=main_loop).start()

    # Start the Telegram bot
    if HEROKU_URL:
        # Deployment on heroku
        PORT = int(os.environ.get("PORT", 8443))
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=BOT_TOKEN,
            webhook_url=HEROKU_URL + BOT_TOKEN,
        )
    else:
        # Local Deployment
        updater.start_polling()

    print("Started")

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == "__main__":
    main()
