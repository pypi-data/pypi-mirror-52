class MobikitException(Exception):
    """generic exception raised from within the mobikit library"""


class AuthException(MobikitException):
    def __init__(self):
        self.message = "You have not passed in a authorization token. Try using mobikit.set_api_key(<your token string>)"
        Exception.__init__(self, self.message)
