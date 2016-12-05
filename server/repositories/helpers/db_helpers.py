import sqlite3


class db_transaction:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.commit()
        self.connection.close()
