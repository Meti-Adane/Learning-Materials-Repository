import ntpath
from api import app
from api.models import Book
from api.admin.validate import validate_arg
from flask_restful import Resource
from flask import json, request, Response


class GetBooks(Resource):

    def get(self):
        search_query = request.args.get("search_query")
        
        if search_query:
            return Response(json.dumps(Book.search(search_query)), status=200)
        
        page = request.args.get("page")
        if page:
            page = int(page)
        else:
            page = 1
        
        limit = request.args.get("limit")
        if limit:
            limit = int(limit)
        else:
            limit = 10
        books = Book.query.paginate(page=page, per_page=limit, error_out=False)
        all_books = books.items

        if len(all_books) == 0:
            return Response(json.dumps({"Message": "No books found"}), status=404)
        
        total_pages = books.pages
        current_page = page

        return Response(json.dumps({"Books": [book.serialize for book in all_books], "totalPages": total_pages, "currentPage": current_page}), status=200)


class GetBook(Resource):

    def get(self, book_id):

        if validate_arg(book_id):
            return validate_arg(book_id)

        book = Book.get_book_by_id(id=book_id)
        if not book:
            return Response(json.dumps({"Message": "Book does not exist"}), status=404)

        return Response(json.dumps(book.serialize),status = 200)

    



class DownloadBook(Resource):
    
    def get(self, book_id):
        if validate_arg(book_id):
            return validate_arg(book_id)

        book = Book.get_book_by_id(id=book_id)
        if not book:
            return Response(json.dumps({"Message": "Book does not exist"}), status=404)
        

        book_path = book.book_file_path
        book_name = ntpath.basename(book_path)
        directory = app.config['BOOK_UPLOAD_FOLDER']
        return book.return_file( book_path)