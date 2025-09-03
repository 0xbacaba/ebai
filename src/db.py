import sqlite3


def setup_db(db_path):
    global db
    global db_cursor
    db = sqlite3.connect(db_path)
    db_cursor = db.cursor()
    _ensure_table_exists("ads", ["id", "name"])
    _ensure_table_exists("errs", ["id", "text"])


def _ensure_table_exists(table: str, fields: [str]):
    tables = db_cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'").fetchone()
    if tables is None:
        fields_str = ', '.join(str(field) for field in fields)
        db_cursor.execute(f"CREATE TABLE {table} ({fields_str})")


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


def has_error(id: int) -> bool:
    res = db_cursor.execute("SELECT 1 FROM errs WHERE id = ?", (id, )).fetchone()
    return res is not None


def insert_error(id: int, text: str):
    db_cursor.execute("INSERT INTO errs VALUES (?, ?)", (id, str(text)))
    db.commit()


def remove_error(id: int):
    db_cursor.execute("DELETE FROM errs WHERE id = ?", (id, ))
    db.commit()


def clear():
    db_cursor.execute("DELETE FROM ads")
    db.commit()
