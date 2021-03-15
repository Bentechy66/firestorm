import typing

from firestorm.db.fields import ForeignKeyField, IntField, PrimaryKeyField, Field
from firestorm.db.sql.modifiers import AutoIncrementModifier, PrimaryKeyModifier
from firestorm.db.table import Table
from firestorm.db.table_mappings import MAPPINGS
from firestorm import session
from firestorm.queryset import QuerySet
from firestorm.session import current_session


class ModelFactory(type):
    def __new__(mcs, name, bases, dct):
        model = super().__new__(mcs, name, bases, dct)

        if not getattr(model, "__annotations__", None):
            return model

        model.model_name = model.get_table_name()
        model.table = Table(model.model_name)
        model.field_classes = model.__annotations__
        model.objects = QuerySet(model)

        mcs.parse_attribute(model, PrimaryKeyField, "id", modifiers=[PrimaryKeyModifier(), AutoIncrementModifier()])

        for field_name in model.field_classes:
            mcs.parse_attribute(model, model.field_classes[field_name], field_name)

        model.field_classes["id"] = PrimaryKeyField

        session.current_session.schema.add_table(model.table)

        return model

    @staticmethod
    def parse_attribute(model, field_type, field_name, modifiers=None):
        if modifiers is None:
            modifiers = []

        if field := MAPPINGS.get(field_type, None):
            model.table.add_field(field(field_name, modifiers=modifiers))

        elif isinstance(field_type, typing._GenericAlias):
            if not getattr(field_type, "modifiers"):
                raise AttributeError("No modifiers found on Modifier!")

            ModelFactory.parse_attribute(
                model,
                field_type.__args__[0],
                field_name,
                modifiers=modifiers + field_type.modifiers
            )

        elif issubclass(field_type, Model):
            model.table.add_field(ForeignKeyField(field_name, field_type, modifiers=modifiers))

        elif issubclass(field_type, Field):
            model.table.add_field(field_type(field_name, modifiers=modifiers))

        else:
            raise AttributeError(f"Couldn't parse attribute {field_name}!")


class Model(metaclass=ModelFactory):
    def __init__(self, *args, **kwargs):
        self.recreate_table()
        for field_name in kwargs:
            setattr(self, field_name, kwargs[field_name])

    def __repr__(self):
        if id := self.table.get_field('id').get_value():
            return f"<{self.model_name}: {id}>"
        return f"<{self.model_name}: Unsaved>"

    def __setattr__(self, key, value):
        for field in self.table.fields:
            if field.name == key:
                return field.set_value(value)
        return super(Model, self).__setattr__(key, value)

    def __getattr__(self, item):
        for field in self.table.fields:
            if field.name == item:
                return field.get_value()

        raise AttributeError(f"Attribute {item} was not found on object!")

    @classmethod
    def get_table_name(cls):
        return cls.__name__

    @classmethod
    def as_create_sql(cls):
        return cls.table.as_create_sql()

    def recreate_table(self):
        self.table = Table(self.model_name)

        for field_name in self.field_classes:
            ModelFactory.parse_attribute(self, self.field_classes[field_name], field_name)

    def save(self):
        if not self.table.needs_save():
            return None
        if self.id is None:
            id = current_session.execute_sql(self.table.as_insert_sql())
            self.table.get_field("id").set_value(id)
        else:
            current_session.execute_sql(self.table.as_update_sql())
        self.table.refresh_field_cache()
