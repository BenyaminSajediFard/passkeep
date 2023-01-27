import sys

from models.users import UserModel

if sys.platform.lower() == "linux":
    try:
        from pysqlcipher3 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3


class ConnectionModel:
    def __init__(self, user: UserModel) -> None:
        self.owner = user.username
        self.password = user.hashed_pass
        self.db_name = user.dbname
        self.connection = self.open_connection()

    def open_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(f"database/.files/{self.db_name}.db")
        connection.execute(f"PRAGMA key='{self.password}'")
        connection.execute("PRAGMA cipher_compatibility = 3")
        return connection

    def select_data(self, search_param=None, item=None):
        # cursor = self.connection.cursor()
        if search_param:
            return self.connection.execute(
                f"SELECT * FROM {self.owner}_data WHERE {search_param}=?", (item,)
            ).fetchall()
        return self.connection.execute(f"SELECT * FROM {self.owner}_data").fetchall()

    def insert_data(self, source: str, password: str):
        try:
            self.connection.execute(
                f"INSERT INTO {self.owner}_data (source, password) VALUES (?, ?)",
                (source, password),
            )
            self.connection.commit()
        except:
            print("got error // INSERT")
            self.close_connection()

    def edit_data(self, id: str, new_source: str, new_password: str):
        try:
            self.connection.execute(
                f"UPDATE {self.owner}_data SET source = ? , password = ? WHERE id = ?",
                (new_source, new_password, id),
            )
            self.connection.commit()
        except:
            print("got error // EDIT")
            self.connection.close()

    def delete_data(self, param=None, item=None):
        if param and item:
            self.connection.execute(
                f"DELETE FROM {self.owner}_data WHERE {param}=?", (item,)
            )
        elif param or item:
            return False
        else:
            self.connection.execute(f"DELETE FROM {self.owner}_data")
        self.connection.commit()

    def close_connection(self):
        self.connection.close()
