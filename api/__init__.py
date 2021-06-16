from config import app_config
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy



BOOK_UPLOAD_FOLDER = 'static/books'
IMAGE_UPLOAD_FOLDER = 'static/images'

IMAGE_ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
BOOK_ALLOWED_EXTENSIONS = {'txt', 'pdf', 'epub', 'mobi'}

app = Flask('__name__')
CORS(app)
jwt = JWTManager(app)
app.config.from_object(app_config['development'])
app.config['BOOK_UPLOAD_FOLDER'] = BOOK_UPLOAD_FOLDER
app.config['IMAGE_UPLOAD_FOLDER'] = IMAGE_UPLOAD_FOLDER
app.config['IMAGE_ALLOWED_EXTENSIONS'] = IMAGE_ALLOWED_EXTENSIONS
app.config['BOOK_ALLOWED_EXTENSIONS'] = BOOK_ALLOWED_EXTENSIONS

app.url_map.strict_slashes = False
app.add_url_rule(
    "/api/book/<book_id>/download", endpoint="return_file", build_only=True
)

db = SQLAlchemy(app)

from api.models import Book, Course, book_resource, User