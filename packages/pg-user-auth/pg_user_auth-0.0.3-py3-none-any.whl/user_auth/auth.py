"""Module Docstring"""

import logging

from flask import request
from flask_rest_api import abort
from jwt import exceptions, decode
from http import HTTPStatus

from config import JWT_KEY


def get_value(key, default=None):
    """ get values from header or url """
    try:
        value = request.headers.get(key, default)
        if not value:
            # only for admin users. not implemented yet
            return request.args.get(key, default)
        return value

    except Exception as e:
        logging.debug(e)
        return None


def decode_jwt(jwt_token):
    """ decode jwt token """
    try:
        return decode(jwt_token, JWT_KEY, algorithms='HS256')
    except exceptions.DecodeError:
        return None


def customer_check(func):
    """Method Docstring for decorators"""

    def gen_header_check(self, *args, **kwargs):
        user = Customer()
        if not user.local_username:
            raise abort(401, message="Unauthorized")
        return func(self, user, *args, **kwargs)

    return gen_header_check


def is_admin_set_customer(user):
    """ check is admin set customer  """
    if user.is_staff and not user.username:
        raise abort(HTTPStatus.BAD_REQUEST,
                    message="Customer not found")


class Customer:
    """Class Docstring"""

    username = None
    server_id = None
    customer_id = None
    is_staff = False
    local_username = None
    user_permissions = None
    groups = None

    def __init__(self, *args, **kwargs):
        # default must false
        # must remove---------
        self.is_staff = request.headers.get('is_staff', False)
        self.username = get_value('username')
        self.server_id = get_value('server_id', 1)
        self.customer_id = get_value('customer_id')
        self.local_username = self.username
        # ---------------------

        del args
        del kwargs
        token_values = decode_jwt(get_value('jwt_token'))
        if token_values:
            self.username = token_values.get('username')
            self.server_id = token_values.get('server_id', 1)
            self.customer_id = token_values.get('customer_id')
            self.is_staff = token_values.get('is_staff', False)
            self.user_permissions = token_values.get('user_permissions')
            self.groups = token_values.get('groups')
            self.local_username = self.username

        if self.is_staff:
            self.username = get_value('username')
            self.server_id = get_value('server_id', 1)
            self.customer_id = get_value('customer_id')
