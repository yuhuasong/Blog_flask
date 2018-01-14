import os

base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.163.com'

    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '18827640740@163.com'

    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'yhs1334'

    MAX_CONTENT_LENGTH = 1024 * 1024 * 2

    UPLOADED_PHOTOS_DEST = os.path.join(base_dir,'static/upload')






    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):

    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(base_dir,'dev-good.sqlite')


class TestingConfig(Config):

    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(base_dir,'test-good.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'pro-good.sqlite')




config = {

    'development': DevelopmentConfig,

    'testing': TestingConfig,

    'production': ProductionConfig,

    'default': DevelopmentConfig

}
























