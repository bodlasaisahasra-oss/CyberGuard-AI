import os
import pymysql
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection


def save_chat(user_id, question, response):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = """
            INSERT INTO chat_history
            (user_id, question, response)
            VALUES (%s, %s, %s)
            """

            cursor.execute(
                sql,
                (user_id, question, response)
            )

        connection.commit()

    finally:
        connection.close()


def get_chat_history(user_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            sql = """
            SELECT question, response, created_at
            FROM chat_history
            WHERE user_id = %s
            ORDER BY created_at ASC
            """

            cursor.execute(sql, (user_id,))

            return cursor.fetchall()

    finally:
        connection.close()