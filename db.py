import os
import sqlite3


def setup_db(db_path):
    db_exists = os.path.exists(db_path)
    global db
    global db_cursor
    db = sqlite3.connect(db_path)
    db_cursor = db.cursor()
    if not db_exists:
        db_cursor.execute("CREATE TABLE ads (id, name)")


def get_ads() -> [(int, str)]:
    return db_cursor.execute("SELECT * FROM ads").fetchall()


def insert_ad(id: int, name: str, commit=True):
    db_cursor.execute("INSERT INTO ads VALUES (?, ?)", (id, name))
    if commit:
        db.commit()


def insert_ads(ads: [(int, str)]):
    for id, name in ads:
        insert_ad(id, name, False)
    db.commit()


def clear():
    db_cursor.execute("DELETE FROM ads")
    db.commit()
