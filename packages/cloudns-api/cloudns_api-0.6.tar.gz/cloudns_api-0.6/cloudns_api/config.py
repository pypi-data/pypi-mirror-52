# -*- coding: utf-8 -*-
#
# name:             config.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       05/27/2019
#

"""
cloudns_api.config
~~~~~~~~~~~~~~~~~~

This module contains the API config constants.
"""

from os import environ


def _is_true(env_var):
    if env_var is None:
        return False
    return env_var.lower() in [1, 'true', 'yes']


CLOUDNS_API_TESTING = _is_true(environ.get('CLOUDNS_API_TESTING'))

CLOUDNS_API_AUTH_ID = environ.get('CLOUDNS_API_AUTH_ID')
if not CLOUDNS_API_AUTH_ID and CLOUDNS_API_TESTING:
    CLOUDNS_API_AUTH_ID = 'test_id'

CLOUDNS_API_AUTH_PASSWORD = environ.get('CLOUDNS_API_AUTH_PASSWORD')
if not CLOUDNS_API_AUTH_PASSWORD and CLOUDNS_API_TESTING:
    CLOUDNS_API_AUTH_PASSWORD = 'test_password'

CLOUDNS_API_DEBUG = _is_true(environ.get('CLOUDNS_API_DEBUG'))
