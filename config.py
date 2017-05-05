import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qVvZ9oTd7plV8rjbovtp'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SUBJECT_PREFIX = 'VarappX'
    EMAIL_ADMIN = '13580484595@163.com'

    DB_USERS = 'users_db2'  # Name of the main database, that stores sessions, db connections etc.

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'varapp_test'
    #MYSQL_PWD = 'pwd'
    SQLALCHEMY_DATABASE_URI = 'mysql://{user}@{host_name}/{DB}'.format(
        user = MYSQL_USER,
        host_name = MYSQL_HOST,
        DB = DB_USERS)
    SQLALCHEMY_BINDS = {
    }
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    SQLITE_DB_PATH = base_dir+'/varappx/main/resources/db'
    DB_TEST = 'demo_mini.db'

    CACHE_TYPE = 'redis'
    CACHE_REDIS_HOST ='127.0.0.1'
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = ''
    CAHCE_REDIS_PASSWORD = ''

    DEBUG = True

    MAIL_SERVER = '220.181.12.16'
    MAIL_PORT = 25
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass


class DeveplomentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = '25'
    MAIL_USE_TLS = True
    MAIL_USER = ''
    MAIL_PASSWD = ''
    SQLALCHEMY_DATABASE_URI ='sqlite:///{db_path}'


class TestingConfig(Config):
    Testing = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'app/main/resources/NY-7_mt2.db')

config  = {
    'development': DeveplomentConfig,
    'testing':Config,
    'default':TestingConfig,
}

