"""
# usage 1, verify token:
from flask import abort
from nezha.pyjwt import is_valid

@app.before_request
def verify_token():
    exclude_paths = (
    "/",
    "/login",
    # ...
    )
    if request.path in exclude_paths:
        return
    token = get_token('token')
    if not is_valid(token, "token_key"):
        return abort(401)

# usage 2 allow abort exception to be thrown:
@app.errorhandler(Exception)
def handle_flask_error(e):
    if request.path.startswith('allow abort exception path'):
        return e
"""
from functools import partial
from flask import json

def json_encoder():
    """
    usage stage: @app.before_app_first_request
    used for: flask.jsonify support datetime/Decimal ...
    :return:
    """
    from nezha.ujson import ComplexEncoder
    json.dumps = partial(json.dumps, cls=ComplexEncoder)