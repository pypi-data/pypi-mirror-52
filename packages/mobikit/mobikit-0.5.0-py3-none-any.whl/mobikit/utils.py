from mobikit.config import config
from mobikit.exceptions import AuthException
from functools import wraps


def token_required(func):
    @wraps(func)
    def _token_required(*args, **kwargs):
        if config.api_token is None:
            raise AuthException
        return func(*args, **kwargs)

    return _token_required
