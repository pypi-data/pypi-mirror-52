from typing import Tuple, Optional

from flask import request
from nezha.pyjwt import is_valid


def verify_jwt_token(token: str, key: str = '', exclude_paths: Optional[Tuple] = None) -> bool:
    """
    verify token before request
    usage:

    @app.before_request
    def verify_token():
        if not verify_jwt_token('this is token', key='this is secret key'):
            # do some thing ...

    :return:
    """
    if exclude_paths and request.path in exclude_paths:
        return True
    return is_valid(token, key)
