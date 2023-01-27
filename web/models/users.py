import sys
import hashlib

from database.secret import id as secpass
from resources.data import create_data_table

if sys.platform.lower() == "linux":
    try:
        from pysqlcipher3 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3


class UserModel:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.dbname = hashlib.md5(
            self.username.encode("utf-8"), usedforsecurity=False
        ).hexdigest()
        self.hashed_pass = password.split("$")[1]

    def register_user(self):
        with sqlite3.connect(f"database/users.db") as connection:
            c = connection.cursor()
            c.execute(f"PRAGMA key='{secpass}'")
            c.execute(
                """INSERT INTO users(username,password)
                        VALUES (?, ?)""",
                (self.username, self.password),
            )

    def create_user(self):
        create_data_table(self)
        self.register_user()

    @classmethod
    def find_by_username(cls, search_item):
        with sqlite3.connect("database/users.db") as connection:  # type: ignore
            connection.execute(f"PRAGMA key='{secpass}'")
            query = "SELECT * FROM users WHERE username=?"
            result = connection.execute(query, (search_item,)).fetchone()
            return cls(*result) if result else None
