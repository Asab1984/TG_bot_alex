import sqlite3 as sq


def create_database():
    global base, cur
    base = sq.connect("database/articles_db.db")
    cur = base.cursor()
    if base:
        print('DB connection = Done')
    base.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            image TEXT,
            title TEXT,
            text TEXT,
            published_at DATETIME)
        """)
    base.commit()


def add_to_db(data):
    cur.execute("""
        INSERT INTO articles VALUES (?, ?, ?, ?)
        """, tuple(data.values()))
    base.commit()


def read_db():
    data = cur.execute("""SELECT * FROM articles""").fetchall()
    return data
