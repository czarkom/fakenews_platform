import os


class Config(object):
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 6969
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


class ProductionConfig(Config):
    DEBUG = os.environ.get("DEBUG")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    DB_HOST = os.environ.get("DB_HOST")
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")


class DevelopmentConfig(Config):
    DEBUG = os.environ.get("DEBUG")
    FLASK_ENV = os.environ.get("FLASK_ENV")
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")