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

x = Author(name="John")
y = Book(name="ben", author=x)
y.price = 37

x.save()
y.save()

book = Book.objects.all()[0]
print(book.author.name)
print(book.price)
