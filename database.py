import psycopg2
from psycopg2 import Error
import os

from getLang import *


def connectPostgre():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn


def closeConnection(conn, cursor=None):
    if cursor is not None:
        cursor.close()
    conn.close()


def getTelegramUser(conn, user_id=None):
    cursor = conn.cursor()
    query = "SELECT * FROM telegram_users "
    if user_id is not None:
        query = query + f"WHERE user_id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall() #fetchone, fetchall, fetchmany


def insertTelegramUsers(conn, user_id, chat_id=None, username=None, admin=None, lang=None):
    try:
        cursor = conn.cursor()
        query = "INSERT INTO telegram_users (user_id, chat_id, username, admin, lang) " \
                "VALUES(%s,%s, %s, %s, %s)"
        args = (user_id, chat_id, username, admin, lang)
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
        conn.commit()

    except Error as error:
        print(error)


def getStudent(conn, user_id=None, number_id=None):
    cursor = conn.cursor()
    query = "SELECT * FROM students "
    if user_id is not None:
        query = query + f"WHERE user_id = {user_id}"
    elif number_id is not None:
        query = query + f"WHERE user_id = {number_id}"
    cursor.execute(query)
    return cursor.fetchall() #fetchone, fetchall, fetchmany


def insertStudent(conn, user_id, number_id, name=None, surname=None, faculty=None, lichess_username=None, chess_username=None, fide_elo=None):
    try:
        cursor = conn.cursor()
        if getStudent(conn, user_id):
            query = f"UPDATE students SET user_id = %s, number_id = %s, name = %s, surname = %s, faculty = %s, lichess_username = %s, chess_username = %s, fide_elo = %s WHERE user_id = {user_id}"
        else:
            query = "INSERT INTO students (user_id, number_id, name, surname, faculty, lichess_username, chess_username, fide_elo) " \
                    "VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        args = (user_id, number_id, name, surname, faculty, lichess_username, chess_username, fide_elo)
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
        conn.commit()

    except Error as error:
        print(error)


if __name__ == '__main__':

    pass
