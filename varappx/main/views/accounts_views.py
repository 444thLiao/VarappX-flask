from flask import jsonify,abort,Response,make_response,request
import os
from varappx.handle_config import settings
from functools import wraps
#from flask_jwt import jwt_required
from .. import main
from flask_login import login_required
#from .auth_views import protected
DAY_IN_SECONDS = 86400
TOKEN_DURATION = DAY_IN_SECONDS / 4
SECRET_KEY = settings.SECRET_KEY


SUPERUSER = 'superuser'
ADMIN = 'admin'
HEAD = 'head'
GUEST = 'user'
DEMO = 'demo'

SUPERUSER_LEVEL = 1
ADMIN_LEVEL = 2
HEAD_LEVEL = 3
GUEST_LEVEL = 4
DEMO_LEVEL = 5



def premission_required(func):
    from flask import current_app
    from flask_login import current_user
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in ['OPTIONS']:
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.role.rank <= func.__defaults__[1]:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)
    return decorated_view

def add_response_headers(headers={}):
    """This decorator adds the headers passed in to the response"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp
        return decorated_function
    return decorator

def cors_handle(f):
    """This decorator passes X-Robots-Tag: noindex"""
    @wraps(f)
    @add_response_headers({'Access-Control-Allow-Origin': '*'})
    def decorated_function(*args, **kwargs):
        return f(*args, **kwargs)
    return decorated_function

def JWT_user(user, duration=TOKEN_DURATION):
    from varappx.main.view_tools.authenticate import set_jwt
    from varappx.main.auth_model_op.user_op import user_factory
    """Set a JWT with user info (username, code, email, etc.), and return it in a json response"""
    user_info = user_factory(user).expose()
    id_token = set_jwt(user_info, SECRET_KEY, duration)
    # example: user_info = {'username': 'admin', 'role': {'can_validate_user': 1, 'name': 'superuser', 'rank': 1, 'can_delete_user': 1}, 'email': 'l0404th@gmail.com', 'firstname': 'Tianhua', 'databases': [{'name': 'NY-7_mt2', 'description': '', 'users': ['admin'], 'size': 182466560}], 'exp': 1493019921, 'code': 'admin', 'isActive': 1, 'lastname': 'Liao'}
    return id_token

def auto_process_OPTIONS(request):
    if request.method == 'OPTIONS':
        resp = Response('test')
        mime_res = {
            'Access-Control-Allow-Origin': "*",
            'Access-Control-Allow-Headers': 'x-requested-with, content-type, accept, origin, authorization, x-csrftoken',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, PATCH, DELETE, OPTIONS',
            'Access-Control-Max-Age': TOKEN_DURATION}
        for _k, _v in mime_res.items():
            resp.headers.setdefault(_k, _v)
        return resp


@main.route('/usersInfo', methods=['OPTIONS', 'POST','GET'])
@cors_handle
@premission_required
def get_users_info(db='demo_mini',rank_required=ADMIN_LEVEL):
    from varappx.main.auth_model_op.user_op import users_list_from_users_db
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    users = [u.expose() for u in users_list_from_users_db(db=db)]
    return jsonify(users)


@main.route('/dbsInfo', methods=['OPTIONS', 'POST','GET'])
@cors_handle
@premission_required
def get_dbs_info(db='demo_mini', rank_required=ADMIN_LEVEL):
    from varappx.main.auth_model_op.user_op import databases_list_from_users_db
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    dbs = [d.expose() for d in databases_list_from_users_db(db=db)]
    return jsonify(dbs)


@main.route('/rolesInfo', methods=['OPTIONS', 'POST','GET'])
@cors_handle
@premission_required
def get_roles_info(db='demo_mini', rank_required=ADMIN_LEVEL):
    from varappx.main.auth_model_op.user_op import roles_list_from_users_db
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    roles = [role.name for role in roles_list_from_users_db(db=db)]
    return jsonify(roles)

@main.route('/signup', methods=['OPTIONS', 'POST'])
@cors_handle
def signup(email_to_file=None):
    """Adds a new -inactive- user to the db. Send an email to an admin to validate the account.
    Not @protected because the user is unidentified at this point.
    """
    from varappx.main.view_tools import authenticate as auth
    #logger.info("Signing up")
    #import pdb;pdb.set_trace()
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    username = request.form['username']
    password = request.form['password']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    phone = request.form['phone']
    if '_functest_' in username:
        email_to_file = open(os.devnull, 'w')
    user,msg = auth.create_user(username, password, firstname, lastname, email, phone, email_to_file)
    if user is None:
        return abort(msg)

    id_token = JWT_user(user, TOKEN_DURATION)
    return jsonify({'id_token': id_token})

@main.route('/resetPasswordRequest', methods=['OPTIONS', 'POST'])
@cors_handle
def reset_password_request(request, email_to_file=None):
    """Does not actually change the password, but sends the user an email
    with a link to the change_password view to generate a new random one.
    Not @protected because the user is unidentified at this point.
    """
    from varappx.main.view_tools import authenticate as auth
    #logger.info("Reset password request")
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    username = request.form['username']
    email = request.form['email']
    host = request.form['host']
    if username == 'test':
        email_to_file = open(os.devnull, 'w')
    user,msg = auth.reset_password_request(username, email, host, email_to_file)
    if user is None:
        return abort(msg)
    user_info = {'username':username, 'email':email}
    return jsonify(user_info)


@main.route('/changePassword', methods=['OPTIONS', 'POST'])
@cors_handle
def change_password(request, new_password=None, email_to_file=None):
    """Change a user's password and sends him an email with the new login.
    Also to validate password reset, in which case it replaces the user's password
    by a random one (if *password* is not set).
    Not @protected because the user is unidentified at this point,
    but the activation code is the protection.
    """
    from varappx.main.view_tools import authenticate as auth
    from varappx.common import utils
    #logger.info("Reset password validation")
    username = request.form['username']
    email = request.form['email']
    activation_code = request.form['activation_code']
    if new_password is None:
        new_password = utils.random_string(10)
    user,msg = auth.change_password(username, email, activation_code, new_password, email_to_file)
    if user is None:
        return abort(msg)
    id_token = JWT_user(user, TOKEN_DURATION)
    return jsonify({'id_token': id_token})

@main.route('/changeAttribute', methods=['OPTIONS', 'POST','GET'])
@cors_handle
@premission_required
def change_attribute(user=None, rank_required=GUEST_LEVEL):
    """Change a user attribute such as email, role, etc."""
    from varappx.main.view_tools import authenticate as auth
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    username = request.form['username']
    code = request.form['code']
    attribute = request.form['attribute']
    new_value = request.form['new_value']
    #logger.info("Change attribute '{}'".format(attribute))
    mod_user,msg = auth.change_attribute(username, code, attribute, new_value)
    # If the user changes himself, need to query again with possible changes
    if user.username == username and user.code == code:
        if attribute == 'username':
            user = auth.find_user(new_value, code)
        elif attribute == 'code':
            user = auth.find_user(username, new_value)
        else:
            user = auth.find_user(username, code)
    # If the user changes another user, check that he has the right to do it
    elif user.role.rank > 2:
        return abort("Insufficent credentials")
    id_token = JWT_user(user, TOKEN_DURATION)
    return jsonify({'id_token': id_token})

@main.route('/userActivation', methods=['OPTIONS', 'POST','GET'])
@cors_handle
@premission_required
def user_activation(email_to_file=None, rank_required=ADMIN_LEVEL):
    """Activate a user's account"""
    from varappx.main.view_tools import authenticate as auth
    #logger.info("Activate/deactivate user")
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    username = request.form['username']
    code = request.form['code']
    email = request.form['email']
    activate = request.form['activate']
    auth.user_activation(username, code, email, activate, email_to_file)
    return Response('')

@main.route('/deleteUser', methods=['OPTIONS', 'POST','GET'])
@cors_handle
@premission_required
def delete_user(request, rank_required=ADMIN_LEVEL):
    from varappx.main.view_tools import authenticate as auth
    #logger.info("Delete user")
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    username = request.form['username']
    code = request.form['code']
    auth.delete_user(username, code)
    return Response('')

@main.route('/attributeDb', methods=['OPTIONS', 'POST','GET'])
@cors_handle
@premission_required
def attribute_db(request, user=None, rank_required=ADMIN_LEVEL):
    from varappx.main.view_tools import authenticate as auth
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    username = request.form['username']
    code = request.form['code']
    dbname = request.form['dbname']
    add = request.form['add']
    #logger.info("Attribute db '{}' to '{}'".format(dbname, username))
    auth.attribute_db(username, code, dbname, add)
    id_token = JWT_user(user, TOKEN_DURATION)
    return jsonify({'id_token': id_token})

