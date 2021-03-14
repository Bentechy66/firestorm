class Table:
    def __init__(self, name, fields=None):
        if fields is None:
            fields = []
        self.fields = fields
        self.name = name

    def as_create_sql(self):
        sql = f"CREATE TABLE {self.name}("
        sql += ",\n".join([field.as_create_sql() for field in self.fields])
        sql += ");"
        return sql

    def add_field(self, field):
        self.fields.append(field)
