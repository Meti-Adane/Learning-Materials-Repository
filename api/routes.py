from flask import Blueprint
from flask_restful import Api
from api.books.books import GetBooks, GetBook, DownloadBook
from api.admin.adminstrator import AddBook
from api.courses.courses import GetCourses, GetCourse
from api.auth.authenticate import Register, Login, Logout, ResetPassword

mod = Blueprint('api', __name__)
api = Api(mod)



api.add_resource(GetBooks, '/api/books')
api.add_resource(GetBook, '/api/book/<book_id>')
api.add_resource(DownloadBook, '/api/book/<book_id>/download')
api.add_resource(GetCourses, '/api/courses')
api.add_resource(GetCourse, '/api/course/<course_id>')

api.add_resource(AddBook, '/api/books')

api.add_resource(Register, '/api/auth/register')
api.add_resource(Login, '/api/auth/login')
api.add_resource(Logout, '/api/auth/logout')
api.add_resource(ResetPassword, '/api/auth/reset-password')