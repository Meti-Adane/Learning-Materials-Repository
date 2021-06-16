from api import jwt
from api.admin.validate import validate_arg
from api.models import Book, User
from flask_restful import Resource
from flask import json, request, Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.datastructures import ImmutableMultiDict
import json



class AddBook(Resource):

    @jwt_required
    def post(self):

        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)

        if user:
            if user.is_admin:
                data = json.loads(request.form.get('data'))

                files = request.files
                print(data)
                print(data["title"])

                if len(data['isbn']) not in (10, 13):
                    return Response(json.dumps({"Message": "Invalid ISBN"}), status=403)
                isbn = Book.query.filter_by(isbn=data['isbn']).first()
                if isbn:
                    return Response(json.dumps({"Message": "Book already exists"}), status=409)
                
                Book(data['title'], data['author'], data['isbn'],
                    data['publisher'], data['description'], data['publish_date'], data['edition'],
                    files['image_file'], data['skill_level'], files['book_file']).save()
                
                book = Book.query.filter_by(isbn=data['isbn']).first()

                return Response(json.dumps({"Message": "Book Created successfully", "Book": book.serialize}), status=201)

            return Response(json.dumps({"Message": "Unauthorized Action."}), status=401)
        
        return Response(json.dumps({"Message": "User does not exist"}), status=404)



class BookOps(Resource):
    @jwt_required
    def put(self, book_id):
        """Function serving edit book api endpoint"""
        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)
        if validate_arg(book_id):
            return validate_arg(book_id)
        if user:
            if user.is_admin:
                book = Book.get_book_by_id(book_id)
                if book:
                    data = json.loads(request.form.get('data'))
                    #data = request.get_json(self)
                    files = request.files


                    book.title = data['title']
                    book.author = data['author']
                    book.isbn = data['isbn']
                    book.publisher = data['publisher']
                    book.description = data['description']
                    book.publish_date = data['publish_date']
                    book.edition = data['edition']
                    book.image_file = book.save_book_image(files['image_file'])
                    book.skill_level = data['skill_level']
                    book.book_file_path = book.save_book_file(files['book_file'])
                    
                    book.save()
                    book = Book.get_book_by_id(book_id)
                    return Response(json.dumps({"Message": "Book updated successfully", "Book": book.serialize}), status=200)
                return Response(json.dumps({"Message": "Book does not exist"}), status=404)
            return Response(json.dumps({"Message": "User not an admin"}), status=401)
        return Response(json.dumps({"Message": "User does not exist"}), status=404)