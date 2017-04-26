from flask import Blueprint

main = Blueprint('main',__name__)

from . import view,errors
#from .views import auth_views
#from .views import accounts_views



