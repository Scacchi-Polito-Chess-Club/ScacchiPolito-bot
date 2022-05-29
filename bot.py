import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

import os
import database
import credentials

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text("Hello")


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def get(update, context):
    conn = database.connectPostgre()
    rows = database.fetch(conn)

    for row in rows:
        update.message.reply_text(row)
    return


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    updater = Updater(credentials.TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("get", get))

    # log all errors
    dp.add_error_handler(error)

    #Webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=credentials.TOKEN)
    updater.bot.setWebhook('https://bot-testingyeah.herokuapp.com/' + credentials.TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()