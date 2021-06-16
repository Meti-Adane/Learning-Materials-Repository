from api import jwt
from admin.validate import valdiate_arg
from api.models import Book, User
from flask_restful import Resource
from flask import json, request, Response
from flask_jwt_extended import get_jwt_identity, jwt_required



class AddBook(Resource):

    @jwt_required
    def post(self):

        current_user = get_jwt_identity()
        user = User.get_user_by_username(current_user)

        if user:
            if user.is_admin:
                data = request.get_json(self)

                if len(data['isbn']) not in (10, 13):
                    return Response(json.dumps({"Message": "Invalid ISBN"}), status=403)
                isbn = Book.query.filter_by(isbn=data['isbn']).first()
                if isbn:
                    return Response(json.dumps({"Message": "Book already exists"}), status=409)
                
                Book(data['title'], data['author'], data['isbn'],
                    data['publisher'], data['description'], data['publish_date'], data['edition'],
                    data['image_file'], data['skill_level'], data['book_file']).save()
                
                book = Book.query.filter_by(isbn=data['isbn']).first()

                return Response(json.dumps({"Message": "Book Created successfully", "Book": book.serialize}), status=201)

            return Response(json.dumps({"Message": "Unauthorized Action."}), status=401)
        
        return Response(json.dumps({"Message": "User does not exist"}), status=404)