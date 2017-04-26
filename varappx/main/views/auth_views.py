from varappx.handle_config import settings
from flask import render_template, request, Response, jsonify
from flask_login import login_required, login_user
from functools import wraps
from flask import make_response,abort

from .. import main

DAY_IN_SECONDS = 86400
TOKEN_DURATION = DAY_IN_SECONDS / 4
SECRET_KEY = settings.SECRET_KEY


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
    @add_response_headers({'Access-Control-Allow-Origin': '*',
                           })
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

class protected:
    """Decorator to force a view to verify the JWT and the existence of the user in the db.
    If the JWT is validated, anyway it was issued here with a valid user,
    but we can check he *still* exists and still has access to that db.
    Protected views can make use of the 'user' keyword argument, binding the User calling the view.
    """


    def __init__(self, view, level=999):
        """:param level: if the user's rank is greater than this, the user cannot access the view."""
        self.view = view
        self.level = level

    def __call__(self, request, **kwargs):
        # Check the token validity
        import varappx.main.view_tools.authenticate as auth
        from varappx.models.users import VariantsDb
        from varappx.common.manage_dbs import deactivate_if_not_found_on_disk,update_if_db_changed
        auth_header = request.environ.get('HTTP_AUTHORIZATION')
        payload,msg = auth.verify_jwt(auth_header, SECRET_KEY)
        if payload is None:
            return abort(msg)
        ## Check that the user exists
        username = payload['username']
        code = payload['code']
        if not auth.check_user_exists(username, code):
            return abort(
                "No account was found with username '{}'.".format(payload['username'])
            )
        user = auth.find_user(username, code)
        # Check user role
        if user.role.rank > self.level:
            return abort("This action requires higher credentials")
        # Check db access
        if kwargs.get('db'):
            dbname = kwargs['db']
            vdb = VariantsDb.query.filter_by(name=dbname, is_active=1).first()
            if vdb is None:
                return abort(
                    "Database '{}' does not exist or is not active anymore.".format(dbname))
            deac = deactivate_if_not_found_on_disk(vdb)
            if deac:
                return abort(
                    "Database '{}' was not found on disk and deactivated.".format(dbname))
            changed = update_if_db_changed(vdb)
            if changed:
                return abort(
                    "Database '{}' has been modified. Please reload.".format(dbname))
            if not auth.check_can_access_db(user, dbname):
                return abort(
                    "User '{}' has no database called '{}'.".format(username, dbname))
        kwargs['user'] = user
        return self.view(request, **kwargs)


@main.route('/authenticate', methods=['OPTIONS', 'POST'])
@cors_handle
def authenticate():
    from varappx.main.view_tools.authenticate import check_credentials
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    if request.method == 'POST':
        usersname = request.form['username']
        passwords = request.form['password']
        user, msgs = check_credentials(usersname, passwords)
        if not user:
            pass
        else:
            login_user(user, remember=True)
            id_token = JWT_user(user, TOKEN_DURATION)
            return jsonify({'id_token': id_token})

    return render_template('index.html')



@main.route('/renew_token', methods=['OPTIONS', 'POST', 'GET'])
@cors_handle
def renew_token():
    from varappx.main.view_tools.authenticate import verify_jwt, find_user
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)

    auth_header = request.environ.get('HTTP_AUTHORIZATION')
    payload, msg = verify_jwt(auth_header, SECRET_KEY)
    if payload is None:
        return render_template('404.html'), 404
    # This user must exist, but can yet be inactive
    user = find_user(payload['username'], payload['code'], require_active=False)
    id_token = JWT_user(user, TOKEN_DURATION)
    return jsonify({'id_token': id_token})
