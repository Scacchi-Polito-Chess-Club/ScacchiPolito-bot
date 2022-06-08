from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

import database
from database import *


CHOOSE_SETTING, CHOOSE_LANG, START_OVER = range(3)


def settings(update, context):
    settings_keyboard = [
        [InlineKeyboardButton("Language", callback_data='lang')],
        [InlineKeyboardButton("Cancel", callback_data='cancel')],
    ]

    settings_reply_markup = InlineKeyboardMarkup(settings_keyboard)

    update.message.reply_text('Hi! Here you can choose some basic settings:', reply_markup=settings_reply_markup)
    return CHOOSE_SETTING


def settings1(update, context):
    query = update.callback_query
    query.answer()
    settings_keyboard = [
        [InlineKeyboardButton("Language", callback_data='lang')],
        # [InlineKeyboardButton("Cancel", callback_data='cancel')],
    ]

    settings_reply_markup = InlineKeyboardMarkup(settings_keyboard)

    query.edit_message_text('Hi! Here you can choose some basic settings:', reply_markup=settings_reply_markup)
    return CHOOSE_SETTING



def choosingLang(update, context):
    query = update.callback_query
    query.answer()
    langs_keyboard = [
        [InlineKeyboardButton("Italian", callback_data='it')],
        [InlineKeyboardButton("English", callback_data='en')],
        [InlineKeyboardButton("Cancel", callback_data='cancel')],
    ]
    langs_reply_markup = InlineKeyboardMarkup(langs_keyboard)
    query.edit_message_text(
        text="Choose your Language!\nNote, there is not full support in italian yet",
        reply_markup=langs_reply_markup
    )
    return CHOOSE_LANG


def setLang(update, context):
    query = update.callback_query
    conn = connectPostgre()
    database.changeLangUser(conn, update.callback_query.from_user.id, str(query.data))
    query.answer('Done')
    back_keyboard = [
        [InlineKeyboardButton("Back", callback_data='cancel')]
    ]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    query.edit_message_text(
        text= f"Ok! I'll do {query.data}",
        reply_markup=back_reply_markup
    )

    closeConnection(conn)
    return CHOOSE_SETTING


def cancel(update, context):
    query = update.callback_query
    query.answer()
    return ConversationHandler.END
