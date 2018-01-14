from app.views.user import user
from app.views.post import post
from .main import main

DEFAULT_BLUEPRINT= (
    (main,''),
    (user,'/user'),
    (post,'/post')
)



def config_blueprint(app):
    for blue_print , url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blue_print,url_prefix = url_prefix)

