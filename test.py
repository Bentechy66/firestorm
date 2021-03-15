from firestorm.models import Model
from firestorm.session import current_session


class Author(Model):
    name: str


class Book(Model):
    name: str
    price: int
    author: Author


current_session.schema.delete_tables()
current_session.schema.create_tables()

z = Book(name="ben")
x = Book(name="ben2")

# print(z.save())
# print(x.save())
