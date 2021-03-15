from firestorm import session


class Schema:
    def __init__(self, tables=None):
        if tables is None:
            tables = []
        self.tables = tables

    def as_create_sql(self):
        return [table.as_create_sql() for table in self.tables]

    def as_delete_sql(self):
        return [f"DROP TABLE IF EXISTS {table.name};" for table in self.tables]

    def create_tables(self):
        session.current_session.execute_sql(self.as_create_sql())

    def delete_tables(self):
        session.current_session.execute_sql(self.as_delete_sql())

    def get_table(self, name):
        for table in self.tables:
            if table.name == name:
                return table
        raise NameError(f"Couldn't find table {name}")

    def add_table(self, table):
        self.tables.append(table)
