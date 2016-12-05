from .helpers import db_transaction


class GenericRepository:
    table_info = []

    def __init__(self, db_path='game_db'):
        self.db_path = db_path
        query = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(*self.table_info)
        with db_transaction(self.db_path) as cursor:
            cursor.execute(query)

    def exec_query(self, query, params):
        with db_transaction(self.db_path) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
