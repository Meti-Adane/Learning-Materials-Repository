from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from api import db
from sqlalchemy import orm


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), index=True)
    author = db.Column(db.String(100), index=True)
    isbn = db.Column(db.String(100), index=True, unique=True)
    publisher = db.Column(db.String(100), index=True)
    publish_date = db.Column(db.Date)
    edition = db.Column(db.String(50))
    description = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False, default='book_default.jpg')
    skill_level = db.Column(db.String(20))

    def __init__(self, title, author, isbn, publisher, quantity):
        """Init function"""
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.quantity = quantity

    @staticmethod
    def get_all_books():
        """Gets all book"""
        return Book.query.all()

    @staticmethod
    def get_book_by_id(id):
        """Gets book by id"""
        return Book.query.filter_by(id=id).first()

    @staticmethod
    def search(q):
        books = Book.query.filter(
            or_(Book.title.like('%'+q.title()+'%'))).all()
        return {"Books": [book.serialize for book in books]}

    @property
    def serialize(self):
        """Serializes book information"""
        if self.quantity == 0:
            self.availability = False
        else:
            self.availability = True
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publisher": self.publisher,
            "availability": self.availability,
            "quantity": self.quantity
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