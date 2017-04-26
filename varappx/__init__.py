from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from .handle_config import settings
from flask_login import LoginManager


db = SQLAlchemy()
mail = Mail()
redis_storge = FlaskRedis()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.authenticate'

def create_app(config_object = settings):
    app = Flask(__name__)
    app.config.from_object(config_object)
    config_object.init_app(app)

    mail.init_app(app)
    db.init_app(app)
    redis_storge.init_app(app)
    login_manager.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint,url_prefix = '/varappx')
    return app

