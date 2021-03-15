from firestorm.models import Model
from firestorm.session import session


class Author(Model):
    name: str


class Book(Model):
    name: str
    price: int
    author: Author


print(session.schema.as_create_sql())
z = Book(name="ben")
x = Book(name="ben2")

print(z.save())
print(x.save())
