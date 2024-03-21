from util.credentialsdetails import get_secret
from util.httpcaller import get_session


class TenableConfig:

    def __init__(self):
        self.access_key = get_secret("tenable_access_key")
        self.secret_key = get_secret("tenable_secret_key")

    def get_header_token(self):
        key = "X-ApiKeys"
        value = "accessKey={accessKey}; secretKey={secretKey}".format(
            accessKey=self.access_key,
            secretKey=self.secret_key)
        return {key: value}

    def get_session(self):
        header = self.get_header_token()
        return get_session(header)
