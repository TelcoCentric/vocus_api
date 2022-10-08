import os

VOCUS_USERNAME = os.environ.get('VOCUS_USERNAME', None)
VOCUS_PASSWORD = os.environ.get('VOCUS_PASSWORD', None)
VOCUS_BASE_URL = os.environ.get('VOCUS_BASE_URL', None)

class UsernameMissingError(Exception):
    pass

class PasswordMissingError(Exception):
    pass

class BaseURLMissingError(Exception):
    pass

if VOCUS_USERNAME is None:
    raise UsernameMissingError(
        "VOCUS_USERNAME required"
    )

if VOCUS_PASSWORD is None:
    raise PasswordMissingError(
        "VOCUS_PASSWORD required"
    )

if VOCUS_BASE_URL is None:
    raise BaseURLMissingError(
        "VOCUS_BASE_URL required"
    )
