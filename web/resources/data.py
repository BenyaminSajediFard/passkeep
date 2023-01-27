import sys

if sys.platform.lower() == "linux":
    try:
        from pysqlcipher3 import dbapi2 as sqlite3
    except ImportError:
        import sqlite3


def create_dummy_data(user, connection: sqlite3.Cursor):  # type: ignore
    connection.execute(
        f"INSERT INTO {user.username}_data (source, password) VALUES ('test.dummy', 'test1234')"
    )


def create_data_table(user):
    with sqlite3.connect(f"database/.files/{user.dbname}.db") as connection:  # type: ignore
        c = connection.cursor()
        c.execute(f"PRAGMA key='{user.hashed_pass}'")
        c.execute("PRAGMA cipher_compatibility = 3")
        c.execute(
            f"CREATE TABLE IF NOT EXISTS {user.username}_data (id INTEGER PRIMARY KEY, source TEXT, password TEXT)"
        )
        create_dummy_data(user, c)
