import psycopg2


def connectPSQL():
    conn = psycopg2.connect(
        host="localhost",
        database="database",
        user="user",
        password="password"
    )
    c = conn.cursor()