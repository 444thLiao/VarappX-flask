from flask import Blueprint

main = Blueprint('main',__name__)

from flask_cors import CORS

cors = CORS(main, resources={"/*": {"Access-Control-Allow-Origin": "*"}})

from . import view,errors
#from .views import auth_views
#from .views import accounts_views



