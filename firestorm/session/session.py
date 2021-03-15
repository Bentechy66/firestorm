from firestorm.db.schema import Schema
import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class Session:
    def __init__(self):
        self.schema = Schema()
        self.connection = sqlite3.connect("firestorm.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def execute_sql(self, sql):
        print(sql)
        if isinstance(sql, list):
            for statement in sql:
                self.cursor.execute(statement)
        else:
            self.cursor.execute(sql)
        self.connection.commit()
        return self.cursor.lastrowid

    def retrieve_records(self, sql):
        self.cursor.execute(sql)
        records = self.cursor.fetchall()
        return records
