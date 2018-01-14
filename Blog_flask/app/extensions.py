from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
moment = Moment()
migrate = Migrate(db=db)
login_manager = LoginManager()
photos = UploadSet('photos',IMAGES)



def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = '需要登录才可访问'
    login_manager.login_view = 'user.login'
    login_manager.session_protection = 'strong'
    configure_uploads(app,photos)
    patch_request_class(app,size = None)






















