class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'testando'
    SQLALCHEMY_DATABASE_URI = 'postgresql:///wordcount_dev"'

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Postgres2022!@localhost:5432/stock'