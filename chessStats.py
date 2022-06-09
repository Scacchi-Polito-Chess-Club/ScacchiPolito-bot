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
import chessApi


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
        text = f"\nLichess stats - {student_username_lichess}\n\n"
        stat = getLichessStats(student_username_lichess)
        text += f"Bullet: {stat['perfs']['bullet']['rating']}\n"
        text += f"Blitz: {stat['perfs']['blitz']['rating']}\n"
        text += f"Rapid: {stat['perfs']['rapid']['rating']}\n"
        text += f"Puzzle: {stat['perfs']['puzzle']['rating']}\n"
        text += f"Win/Draw/Loss : {stat['count']['win']}/{stat['count']['draw']}/{stat['count']['loss']}\n"
        update.message.reply_text(text)
    if student_username_chess:
        text = f"\nChess stats - {student_username_chess}\n"
        stat = getChessStats(student_username_chess)
        text += f"Bullet: {stat['chess_bullet']['last']['rating']}\n"
        text += f"Blitz: {stat['chess_blitz']['last']['rating']}\n"
        text += f"Rapid: {stat['chess_rapid']['last']['rating']}\n"
        text += f"Tactics (highest): {stat['tactics']['highest']['rating']}\n"
        update.message.reply_text(text)
    closeConnection(conn)
    return


def getChessStats(username):
    stat = chessApi.getPlayerStats(username)
    return stat


def getLichessStats(username):
    stat = lichessApi.getUserPublicData(username)
    return stat



