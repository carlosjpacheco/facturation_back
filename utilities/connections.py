import psycopg2
from sanic.response import json


def connectPSQL():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="invoicing_system",
            user="postgres",
            password="postgres"
        )
        cursor = conn.cursor()
        connection = {
            "cursor":cursor,
            "conn":conn
        }
        return connection  

    except:
        return False

# def connectPSQLLog():
#     try:
#         conn = psycopg2.connect(
#             host="locddalhost",
#             database="invoicing_system",
#             user="admin",
#             password="admin"
#         )
#         cursor = conn.cursor()

#         return cursor  

#     except (Exception, psycopg2.Error) as error:
#         print("Failed trying connect to DB", error)