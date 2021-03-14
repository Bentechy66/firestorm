class Schema:
    def __init__(self, tables=None):
        if tables is None:
            tables = []
        self.tables = tables

    def as_create_sql(self):
        return "\n".join([tables.as_create_sql() for tables in self.tables])

    def add_table(self, table):
        self.tables.append(table)
