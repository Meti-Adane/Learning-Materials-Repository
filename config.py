import os

class Config(object):
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = 'super-secret-key'
    JWT_BLACKLIST_ENABLED = False
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    SQLALCHEMY_DATABASE_URI = os.getenv('FlaskRepositoryDB')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "<Production DB URL>"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('FlaskRepositoryDB')
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "<Testing DB URL>"
    SQLALCHEMY_ECHO = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}