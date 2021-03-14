# from firestorm.db.sql import modifiers
# from firestorm.db.table import Table
# from firestorm.db.schema import Schema
# from firestorm.db.fields import *
#
# class Author:
#     @staticmethod
#     def get_table_name():
#         return "Author"
#
#
# schema = Schema()
#
# author = Table("Author")
# schema.add_table(author)
# author.add_field(IntField("id", modifiers=[modifiers.PrimaryKeyModifier()]))
# author.add_field(TextField("author_name"))
#
# book = Table("Book")
# schema.add_table(book)
# book.add_field(IntField("id", modifiers=[modifiers.PrimaryKeyModifier()]))
# book.add_field(TextField("book_name"))
# book.add_field(ForeignKeyField("author", Author))
#
# print(schema.as_create_sql())
from typing import Callable

from firestorm.models import Model
from firestorm.modifiers import NotNull


class Author(Model):
    name: str


class Book(Model):
    name: str
    price: int
    author: NotNull[Author]


print(Author.as_create_sql())
print(Book.as_create_sql())
