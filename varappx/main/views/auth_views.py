from varappx.handle_config import settings
from flask import render_template, request, Response, jsonify
from flask_login import login_required, login_user
from functools import wraps
from flask import make_response,abort,redirect,flash
from varappx import login_manager
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

@main.route('/authenticate', methods=['OPTIONS', 'POST','GET'])
@cors_handle
def authenticate():
    from varappx.main.view_tools.authenticate import check_credentials
    from varappx.main.view_tools.authenticate import verify_jwt, find_user
    if auto_process_OPTIONS(request):
        return auto_process_OPTIONS(request)
    if 'next' in request.args.keys():
        auth_header = request.environ.get('HTTP_AUTHORIZATION')
        payload, msg = verify_jwt(auth_header, SECRET_KEY)
        if payload:
            user = find_user(payload['username'], payload['code'], require_active=False)
            login_user(user, remember=True)
            next = request.args.get('next')
            return redirect(next)
        else:
            return render_template('404.html'), 404
    if request.method != 'OPTIONS':
        usersname = request.form['username']
        passwords = request.form['password']
        user, msgs = check_credentials(usersname, passwords)
        if not user:
            pass
        else:
            #print(user)
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



