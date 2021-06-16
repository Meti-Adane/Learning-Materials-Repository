from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask import send_from_directory, url_for, send_file
from api import db
from sqlalchemy import or_






class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), index=True)
    author = db.Column(db.String(100), index=True)
    isbn = db.Column(db.String(100), index=True, unique=True)
    publisher = db.Column(db.String(100), index=True)
    description = db.Column(db.Text)
    publish_date = db.Column(db.Date)
    edition = db.Column(db.String(50))
    image_file = db.Column(db.Text)
    skill_level = db.Column(db.String(20))
    book_file_path = db.Column(db.Text)

    def __init__(self, title, author, isbn, publisher, description, publish_date, edition, image_file, skill_level, book_file):
        """Init function"""
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.description = description
        self.publish_date = publish_date
        self.edition = edition
        self.image_file = save_book_image(image_file)
        self.skill_level = skill_level
        self.book_file_path = save_book_file(book_file)
        
        

    @staticmethod
    def get_all_books():
        """Gets all book"""
        return Book.query.all()

    @staticmethod
    def get_book_by_id(id):
        """Gets book by id"""
        return Book.query.filter_by(id=id).first()









    def allowed_file(self, filename, ALLOWED_EXTENSIONS):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def return_file(self, filename):
        print("return_file called")
        return send_file(filename, as_attachment=True)


    @staticmethod
    def save_book_image(image_file):
       
        if image_file and allowed_file(image_file.filename, app.config['IMAGE_ALLOWED_EXTENSIONS']):
            image_filename = secure_filename(image_file.filename)
            full_imagename = os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], image_filename)
            file.save(full_imagename)

        return url_for('return_file', filename=full_imagename, _external=True) #UPLOAD_FOLDER=app.config['IMAGE_UPLOAD_FOLDER'],
    
    @staticmethod
    def save_book_file(book_file):
        
        if book_file and allowed_file(book_file.filename, app.config['BOOK_ALLOWED_EXTENSIONS']):
            book_filename = secure_filename(book_file.filename)
            full_bookname = os.path.join(app.config['BOOK_UPLOAD_FOLDER'], book_filename)
            file.save(full_bookname)

        return url_for('return_file', filename=full_bookname, _external=True) #UPLOAD_FOLDER=app.config['BOOK_UPLOAD_FOLDER']










    @staticmethod
    def search(q):
        books = Book.query.filter(
            or_(Book.title.like('%'+q.title()+'%'))).all()
        return {"Books": [book.serialize for book in books]}

    @property
    def serialize(self):
        """Serializes book information"""
        
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "description":self.description,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "publish_date":self.publish_date,
            "skill_level":self.skill_level,
            "cover_img":self.image_file
        }

    def save(self):
        """Saves book object to database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Deletes book object"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "Book: {}".format(self.title)






book_resource = db.Table('book_resource', db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True), 
db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True))





class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), index=True)
    description = db.Column(db.Text)
    books = db.relationship('Book', secondary=book_resource, backref=db.backref('books'))

    def init(self, title):
        self.title = title

    @staticmethod
    def get_all_courses():

        return Course.query.all()

    @staticmethod
    def get_course_by_id(id):

        return Course.query.filter_by(id=id).first()
    
    @staticmethod
    def search(q):
        courses = Course.query.filter(
            or_(Course.title.like('%'+q.title()+'%'))
        ).all()
        return {"Courses":[course.serialize for course in courses]}

    @property
    def serialize(self):

        return {
            "id": self.id,
            "title":self.title,
            "description":self.description
        }










class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __init__(self, email, username, first_name, last_name, password):
        """Init function"""
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        """Hashes user password"""
        return generate_password_hash(password)

    @staticmethod
    def verify_password(saved_password, password):
        """Check is password hash matches actual password"""
        return check_password_hash(saved_password, password)

    def save(self):
        """Saves user objects to database"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def all_users():
        """Gets all users"""
        return User.query.all()

    @staticmethod
    def get_user_by_username(username):
        """Gets user by username"""
        return User.query.filter_by(username=username).first()

    def update_password(self, password):
        """Updates user's password"""
        self.hash_password = User.hash_password(password)
        User.save(self)

    @property
    def serialize(self):
        """Serializes User object"""
        return {
            "email": self.email,
            "username": self.username,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "is_admin": self.is_admin,
        }

    @property
    def promote(self):
        """Promotes normal user to admin"""
        if self.is_admin == True:
            pass
        self.is_admin = True
        User.save(self)
    
    def admin(self):
        """Checks if user is an admin"""
        if self.is_admin:
            return True
        return False

    def __repr__(self):
        return "User: {}".format(self.username)






class Token(db.Model):
    """Token Model"""
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(1000), index=True, unique=True)
    owner = db.Column(db.String(60))
    created = db.Column(db.DateTime, default=datetime.today())

    def __init__(self, token, owner):
        """Init function"""
        self.token = token
        self.owner = owner

    @staticmethod
    def all_tokens():
        """Gets all tokens"""
        return Token.query.all()

    @staticmethod
    def token_by_owner(username):
        """Gets token by user's username"""
        return Token.query.filter_by(owner=username).first()

    def save(self):
        """Saves generated token to database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete token after being revoked"""
        db.session.delete(self)
        db.session.commit()


class Revoked(db.Model):
    """Revoked Token Table"""

    __tablename__ = 'revoked'
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(1000), index=True)
    date_revoked = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, token):
        """Init function"""
        self.token = token

    @staticmethod
    def is_blacklisted(token):
        """Checks if token is revoked"""
        if Revoked.query.filter_by(token=token).first():
            return True
        return False

    def save(self):
        """Saves revoked token to database"""
        db.session.add(self)
        db.session.commit()