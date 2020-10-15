import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'some secret'
    MAIL_SERVER = 'mail2010vm.irvis.local'
    MAIL_PORT = int('25')
    MAIL_USERNAME = 'kostya@gorgaz.ru'
    UPLOAD_DIR = os.path.join(basedir, 'files')
    ALLOWED_EXT = {'pdf', 'png', 'jpeg', 'jpg', 'doc', 'docx'}
    
    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost/myapp'


config = {
        'production': ProductionConfig,
        'default': ProductionConfig
    }
