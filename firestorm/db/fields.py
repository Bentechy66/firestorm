class Field:
    def __init__(self, name, modifiers=None, value=None, live=False, *args, **kwargs):
        self.name = name
        self.modifiers = modifiers if modifiers else list()
        self.value = value
        self._old_value = self.value

    def get_modifiers_as_sql(self, operation):
        return [modifier.as_sql() for modifier in self.modifiers if operation in modifier.applies_to]

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def needs_save(self):
        return self._old_value != self.value

    def to_sql_repr(self, value):
        return str(self.value)

    def value_as_sql_repr(self):
        return self.to_sql_repr(self.value)

    def as_create_sql(self):
        if not getattr(self, "datatype"):
            raise AttributeError("SQLField must declare datatype attribute!")

        sql_parts = [self.name, self.datatype]
        sql_parts += self.get_modifiers_as_sql("CREATE")
        return " ".join(sql_parts)

    def as_update_sql(self):
        if self.value == self._old_value:
            return None
        return f"{self.name} = {self.value_as_sql_repr()}"


class PrimaryKeyField(Field):
    datatype = "INTEGER"


class TextField(Field):
    datatype = "TEXT"

    def to_sql_repr(self, value):
        return "'" + str(value) + "'"


class IntField(Field):
    datatype = "INTEGER"


class ForeignKeyField(Field):
    datatype = "INTEGER"

    def __init__(self, name, foreign_object, *args, **kwargs):
        super(ForeignKeyField, self).__init__(name, *args, **kwargs)
        self.foreign_object = foreign_object

    def to_sql_repr(self, value):
        if self.value.id is None:
            raise ValueError("Cannot save value since it refers to an unsaved object")
        return str(self.value.id)

    def as_create_sql(self):
        sql = super(ForeignKeyField, self).as_create_sql()
        sql += f", FOREIGN KEY({self.name}) REFERENCES {self.foreign_object.get_table_name()}(id)"
        return sql
