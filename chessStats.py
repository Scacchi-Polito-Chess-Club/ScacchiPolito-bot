from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from database import *
import lichessApi


def getStats(update, context):
    user_id = update.message.from_user.id
    conn = connectPostgre()
    student = getStudent(conn, user_id=user_id)
    if not student:
        update.message.reply_text("You have to set your infos before! Type /student_registration")
        return
    student_username_lichess = student[5]
    student_username_chess = student[6]
    text = "Here you are yours stats! If you want to change your account name use /student_registration\n"
    if student_username_lichess:
        text = "\nLichess stats - \n\n"
        stat = getLichessStats(student_username_lichess)
        text += f"Bullet: {stat['perfs']['bullet']['rating']}\n"
        text += f"Blitz: {stat['perfs']['blitz']['rating']}\n"
        text += f"Rapid: {stat['perfs']['rapid']['rating']}\n"
        text += f"Puzzle: {stat['perfs']['puzzle']['rating']}\n"
        text += f"Win/Draw/Loss : {stat['count']['win']}/{stat['count']['draw']}/{stat['count']['loss']}\n"
    if student_username_chess:
        text = "\nChess stats:\n"
        text += getChessStats(student_username_chess)
        update.message.reply_text(text)
    closeConnection(conn)
    return


def getChessStats(username):
    return "yet to be implemented :("


def getLichessStats(username):
    stat = lichessApi.getUserPublicData(username)
    return stat



