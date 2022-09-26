import os
import requests

VOCUS_USERNAME = os.environ.get('VOCUS_USERNAME', None)
VOCUS_PASSWORD = os.environ.get('VOCUS_PASSWORD', None)

class UsernameMissingError(Exception):
    pass

class PasswordMissingError(Exception):
    pass

if VOCUS_USERNAME is None:
    raise UsernameMissingError(
        "All actions require login username"
    )

if VOCUS_PASSWORD is None:
    raise PasswordMissingError(
        "All actions require login password"
    )

session = requests.Session()

from .vocus import Vocus
Vocus.Login(VOCUS_USERNAME, VOCUS_PASSWORD)
