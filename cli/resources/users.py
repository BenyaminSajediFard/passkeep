import sys

from database.secret import id as secpass

if sys.platform.lower() == "linux":
    try:
        from pysqlcipher3 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3


def create_users_table():
    with sqlite3.connect("database/users.db") as connection:  # type: ignore
        c = connection.cursor()
        c.execute(f"PRAGMA key='{secpass}'")
        # connection.execute("PRAGMA cipher_compatibility = 3")
        c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
