from flask import Blueprint
from flask_restful import Api
from api.books.books import GetBooks, GetBook
from api.courses.courses import GetCourses, GetCourse

mod = Blueprint('api', __name__)
api = Api(mod)


api.add_resource(GetBooks, 'api/books')
api.add_resource(GetBook, 'api/book/<book_id>')
api.add_resource(GetCourses, 'api/courses')
api.add_resource(GetCourse, 'api/course/<course_id>')