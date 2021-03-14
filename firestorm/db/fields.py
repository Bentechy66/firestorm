class Field:
    def __init__(self, name, modifiers=None, *args, **kwargs):
        self.name = name
        self.modifiers = modifiers if modifiers else list()

    def get_modifiers_as_sql(self, operation):
        return [modifier.as_sql() for modifier in self.modifiers if operation in modifier.applies_to]

    def as_create_sql(self):
        if not getattr(self, "datatype"):
            raise AttributeError("SQLField must declare datatype attribute!")

        sql_parts = [self.name, self.datatype]
        sql_parts += self.get_modifiers_as_sql("CREATE")
        return " ".join(sql_parts)


class TextField(Field):
    datatype = "TEXT"


class IntField(Field):
    datatype = "INTEGER"


class ForeignKeyField(Field):
    datatype = "INTEGER"

    def __init__(self, name, foreign_object, *args, **kwargs):
        super(ForeignKeyField, self).__init__(name, *args, **kwargs)
        self.foreign_object = foreign_object

    def as_create_sql(self):
        sql = super(ForeignKeyField, self).as_create_sql()
        sql += f", FOREIGN KEY({self.name}) REFERENCES {self.foreign_object.get_table_name()}(id)"
        return sql
