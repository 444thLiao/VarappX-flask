from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from .handle_config import settings
from flask_login import LoginManager


db = SQLAlchemy()
mail = Mail()
redis_store = FlaskRedis()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.authenticate'



def create_app(config_object = settings):
    app = Flask(__name__)
    app.config.from_object(config_object)
    config_object.init_app(app)

    mail.init_app(app)
    db.init_app(app)
    redis_store.init_app(app)
    login_manager.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint,url_prefix = '/varappx')
    return app


def check_everything():
    import sys
    from varappx.common.db_utils import connection_has_tables
    from varappx.common.manage_dbs import copy_VariantsDb_to_settings
    from varappx.common.utils import check_redis_connection
    from varappx.stats.stats_service import stats_service
    from varappx.handle_init import app
    #from varappx.
    user_db_ready = connection_has_tables(5)
    if user_db_ready and 'migrate' not in sys.argv:
        added_connections = copy_VariantsDb_to_settings()
        redis_ready = check_redis_connection(app)
    if redis_ready:
        pass
        #for dbname in added_connections:
            #stats_service(dbname)
            #genotypes_service(dbname)
            #add_versions(dbname)
    else:
        print("(!) Could not connect to Redis. Make sure Redis is installed, "
                "is up and running (try `redis-cli ping`) "
                "and serves at 127.0.0.1:6379 (or whatever is defined in settings")