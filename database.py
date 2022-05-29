import psycopg2
from psycopg2 import Error
import os




def connectPostgre():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn


def closeConnection(conn, cursor=None):
    if cursor is not None:
        cursor.close()
    conn.close()


def fetch(conn, user_id=None):
    cursor = conn.cursor()
    query = "SELECT * FROM telegram_users "
    if user_id is not None:
        query = query + f"WHERE user_id == {user_id}"

    cursor.execute(query)
    return cursor.fetchall() #fetchone, fetchall, fetchmany


def insertTelegramUsers(conn, user_id, chat_id=None, username=None, admin=None, lang=None):
    try:
        cursor = conn.cursor()
        query = "INSERT INTO telegram_users (user_id, chat_id, username) " \
                "VALUES(%s,%s, %s)"
        args = (user_id, chat_id, username)
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
        conn.commit()

    except Error as error:
        print(error)

    finally:
        if cursor is not None: cursor.close()
        conn.close()


if __name__ == '__main__':
    # insert()
    conn = connectPostgre()
    fetch(conn)
