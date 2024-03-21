from util.credentialsdetails import get_secret, get_config
from util.httpcaller import get_session


class HackerOneConfig:

    def __init__(self):
        self.username = get_config("hacker_one_user_name")
        self.api_token = get_secret("hacker_one_api_token")
        self.program = ["wayfair"]

    def get_session(self):
        session = get_session()
        session.auth = (self.username, self.api_token)
        return session
