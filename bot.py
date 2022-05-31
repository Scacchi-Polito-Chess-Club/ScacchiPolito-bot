import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

import os
import database
import credentials
from studentRegistration import *
from getLang import *

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    conn = connectPostgre()
    user = getTelegramUser(conn, update.message.from_user.id)
    if user:
        lang = user[0][4]
        text = getString(lang, "welcome_back")
    else:
        lang = update.message.from_user.language_code
        text = getString(lang, "welcome")
        insertTelegramUsers(conn, update.message.from_user.id, update.message.chat.id, update.message.from_user.username, 'false', lang )
    update.message.reply_text(text)
    closeConnection(conn)


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def getAll(update, context):
    conn = database.connectPostgre()
    if not getTelegramUser(conn, update.message.from_user.id)[0][3]:
        reply = "Sorry you need admin rigths."
    else:
        rows = database.getTelegramUser(conn)
        reply = ""
        for row in rows:
            reply = reply + str(row) + "\n"
    update.message.reply_text(reply)
    closeConnection(conn)
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
    dp.add_handler(CommandHandler("get_all", getAll))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('student_registration', studentRegistration)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(ID Number|Faculty|Name|Surname|Lichess nickname|Chess nickname|FIDE_ELO)$'),
                    studentRegistrationRegularChoice
                )
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')), studentRegistrationRegularChoice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    studentRegistrationReceivedInformation,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^(Done|Cancel)$'), studentRegistrationDone)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    dp.add_handler(conv_handler)

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