from marshmallow import Schema, fields


class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    description = fields.Str()


class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author


incoming_book_data = {
    "title": "Clean Code",
    "author": "Martin Fowler",
    "description": "A book about writing cleaner code",
}

# book = Book("Clean Code", "Martin Fowler", "A book about writing cleaner code")
# book_schema = BookSchema()
# book_dict = book_schema.dump(book)

book_schema = BookSchema()
book = book_schema(incoming_book_data)
book_obj = Book(**book)
print(book_obj)