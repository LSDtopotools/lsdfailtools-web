from functools import wraps
import os
import requests
from flask import request

URL = os.environ.get("OAUTH_ENDPOINT")

ACTUAL_USER_KEY = "actual_user"


def authorized(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            response = requests.get(
                URL,
                headers={
                    "authorization": request.headers.get("authorization")
                }
            )
            if response.status_code == 200:
                kwargs[ACTUAL_USER_KEY] = response.json()
                return func(*args, **kwargs)
            else:
                return "", 401, {}

        except Exception:
            return "Contact the administrator", 500, {}

    return inner
