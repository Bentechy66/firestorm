from firestorm.queryset import QuerySet


class Field:
    def __init__(self, name, modifiers=None, value=None, *args, **kwargs):
        self.name = name
        self.modifiers = modifiers if modifiers else list()
        self.value = value
        self._old_value = self.value

    def get_modifiers_as_sql(self, operation):
        return [modifier.as_sql() for modifier in self.modifiers if operation in modifier.applies_to]

    def set_value(self, value, from_db=False):
        self.value = value

    def get_value(self):
        return self.value

    def needs_save(self):
        return self._old_value != self.value

    def to_sql_repr(self, value):
        return str(value)

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


class ModelMock:
    # Used in ForeignKeyFields to mock a real field. Gets replaced almost instantly.
    def __init__(self, id):
        self.id = id


class ForeignKeyField(Field):
    datatype = "INTEGER"

    def __init__(self, name, foreign_object, *args, **kwargs):
        super(ForeignKeyField, self).__init__(name, *args, **kwargs)
        self.foreign_object = foreign_object

    def to_sql_repr(self, value):
        if self.value.id is None:
            raise ValueError("Cannot save value since it refers to an unsaved object")
        return str(value.id)

    def set_value(self, value, from_db=False):
        if from_db:
            self.value = ModelMock(value)
        else:
            self.value = value

    def get_value(self):
        return QuerySet(self.foreign_object).filter(id=self.value.id).all()[0]

    def as_create_sql(self):
        sql = super(ForeignKeyField, self).as_create_sql()
        sql += f", FOREIGN KEY({self.name}) REFERENCES {self.foreign_object.get_table_name()}(id)"
        return sql
