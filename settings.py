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
    conn = connectPostgre()
    lang = getTelegramUser(conn, update.message.from_user.id)[0][4]
    closeConnection(conn)
    settings_keyboard = [
        [InlineKeyboardButton(getString(lang, "language"), callback_data='lang')],
        [InlineKeyboardButton(getString(lang, "exit"), callback_data='exit')],
    ]

    settings_reply_markup = InlineKeyboardMarkup(settings_keyboard)

    update.message.reply_text(getString(lang, "setting"), reply_markup=settings_reply_markup)
    return CHOOSE_SETTING


def settings1(update, context):
    conn = connectPostgre()
    lang = getTelegramUser(conn, update.callback_query.from_user.id)[0][4]
    closeConnection(conn)
    query = update.callback_query
    query.answer()
    settings_keyboard = [
        [InlineKeyboardButton(getString(lang, "language"), callback_data='lang')],
        [InlineKeyboardButton(getString(lang, "exit"), callback_data='exit')],
    ]

    settings_reply_markup = InlineKeyboardMarkup(settings_keyboard)

    query.edit_message_text(getString(lang, "setting"), reply_markup=settings_reply_markup)
    return CHOOSE_SETTING



def choosingLang(update, context):
    conn = connectPostgre()
    lang = getTelegramUser(conn, update.callback_query.from_user.id)[0][4]
    closeConnection(conn)
    query = update.callback_query
    query.answer()
    langs_keyboard = [
        [InlineKeyboardButton(getString(lang, "italian"), callback_data='it')],
        [InlineKeyboardButton(getString(lang, "english"), callback_data='en')],
        [InlineKeyboardButton(getString(lang, "back"), callback_data='back')],
    ]
    langs_reply_markup = InlineKeyboardMarkup(langs_keyboard)
    query.edit_message_text(
        text=getString(lang, "lan_choose_language"),
        reply_markup=langs_reply_markup
    )
    return CHOOSE_LANG


def setLang(update, context):
    query = update.callback_query
    conn = connectPostgre()
    database.changeLangUser(conn, update.callback_query.from_user.id, str(query.data))
    lang = getTelegramUser(conn, update.callback_query.from_user.id)[0][4]
    query.answer(getString(lang, "done"))
    back_keyboard = [
        [InlineKeyboardButton(getString(lang, "back"), callback_data='back')],
        [InlineKeyboardButton(getString(lang, "exit"), callback_data='exit')],
    ]
    back_reply_markup = InlineKeyboardMarkup(back_keyboard)
    query.edit_message_text(
        text= f"Okay!",
        reply_markup=back_reply_markup
    )

    closeConnection(conn)
    return CHOOSE_SETTING


def settingsClose(update, context):
    query = update.callback_query
    query.delete_message()
    return ConversationHandler.END