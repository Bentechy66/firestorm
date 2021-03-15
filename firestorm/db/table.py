from firestorm.db.sql.filter import ExactFieldFilter


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

    def needs_save(self):
        for field in self.fields:
            if field.needs_save():
                return True
        return False

    def as_update_sql(self):
        sql = f"UPDATE {self.name} SET "
        sql += ", ".join([field.as_update_sql() for field in self.fields if field.as_update_sql() is not None])
        sql += " WHERE " + ExactFieldFilter(self.get_field("id")).as_sql() + ";"

        return sql

    def add_field(self, field):
        self.fields.append(field)

    def get_field(self, name):
        for field in self.fields:
            if field.name == name:
                return field

        raise AttributeError(f"Cannot find field {name}")
