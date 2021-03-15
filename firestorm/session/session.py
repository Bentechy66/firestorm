from firestorm.db.schema import Schema
import sqlite3


class Session:
    def __init__(self):
        self.schema = Schema()
        self.connection = sqlite3.connect("firestorm.db")
        self.cursor = self.connection.cursor()

    def execute_sql(self, sql):
        print(sql)
        if isinstance(sql, list):
            for statement in sql:
                self.cursor.execute(statement)
            return
        return self.cursor.execute(sql)
