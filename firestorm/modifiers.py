from typing import TypeVar, Generic

from firestorm.db.sql.modifiers import NotNullModifier, PrimaryKeyModifier, AutoIncrementModifier

T = TypeVar('T')


class NotNull(Generic[T]):
    modifiers = [NotNullModifier()]


class AutoIncrement(Generic[T]):
    modifiers = [AutoIncrementModifier()]


class PrimaryKey(Generic[T]):
    modifiers = [PrimaryKeyModifier()]
