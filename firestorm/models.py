import typing

from firestorm.db.fields import ForeignKeyField, IntField
from firestorm.db.sql.modifiers import AutoIncrementModifier, PrimaryKeyModifier
from firestorm.db.table import Table
from firestorm.db.table_mappings import MAPPINGS
from firestorm.modifiers import NotNull


class ModelFactory(type):
    def __new__(mcs, name, bases, dct):
        model = super().__new__(mcs, name, bases, dct)

        if not getattr(model, "__annotations__", None):
            return model

        model.name = model.get_table_name()
        model.table = Table(model.name)
        model.field_classes = model.__annotations__

        mcs.parse_attribute(model, int, "id", modifiers=[AutoIncrementModifier(), PrimaryKeyModifier()])

        for field_name in model.field_classes:
            mcs.parse_attribute(model, model.field_classes[field_name], field_name)

        model.field_classes["id"] = int

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

        else:
            raise AttributeError(f"Couldn't parse attribute {field_name}!")


class Model(metaclass=ModelFactory):
    @classmethod
    def get_table_name(cls):
        return cls.__name__

    @classmethod
    def as_create_sql(cls):
        return cls.table.as_create_sql()
