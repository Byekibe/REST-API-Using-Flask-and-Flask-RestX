from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields, marshal, marshal_with_field
from models import db, app, Book

api=Api(app, doc="/", title="A book API", description="A simple book rest Api")

book_model=api.model(
    'Book', 
    {
        'id':fields.Integer(),
        'title': fields.String(),
        'author': fields.String(),
        "date_added": fields.String(),
    }
)

@api.route("/books")
class Books(Resource):
    @api.marshal_list_with(book_model, code=200, envelope="books")
    def get(self):
        ''' Get all Books'''
        books = Book.query.all()
        return books
    
    @api.marshal_list_with(book_model, code=201, envelope="book")
    # @api.doc(params={'title': 'A title', 'author': "An author"})
    def post(self):
        ''' Create a new book '''
        data = request.get_json()

        title = data.get('title')
        author = data.get('author')
        new_book = Book(title=title, author=author)

        db.session.add(new_book)
        db.session.commit()

        return new_book 


@api.route("/book/<int:id>")
class BookResource(Resource):
    @api.marshal_list_with(book_model, code=200, envelope="book")
    def get(self, id):
        ''' Get a book by id '''
        book=Book.query.get_or_404(id)
        return book, 200
    
    @api.marshal_with(book_model, 200, envelope="book")
    def put(self, id):
        '''Update a book'''
        book_to_update = Book.query.get_or_404(id)

        data = request.get_json()

        book_to_update.title = data.get('title')    
        book_to_update.author = data.get('author')

        db.session.commit()

        return book_to_update,200

    @api.marshal_with(book_model, code=200, envelope="book_deleted")
    def delete(self, id):
        '''Delete a book'''
        book_to_delete = Book.query.get_or_404(id)
        db.session.delete(book_to_delete)
        db.session.commit()

        return book_to_delete, 200

@app.shell_context_processor
def make_shell_context():
    return {
        'db':db,
        'Book':Book
    }



if __name__=="__main__":
    app.run(port=7000, debug=True)
