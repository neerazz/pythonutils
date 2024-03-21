from tools.hackerone.hackerone_config import HackerOneConfig
from tools.hackerone.hackerone_util import getQueryParams


class HackerOneClient:
    base_url = "https://api.hackerone.com/v1"
    urls = {
        "": base_url,
        "reports": base_url + "/reports"
    }

    def __init__(self):
        self.config = HackerOneConfig()
        self.program = self.config.program

    def make_request(self, url):
        session = self.config.get_session()
        response = session.get(url)
        return response.json()

    def get_call(self, url: str, query_param: dict = None):
        if query_param is None:
            query_param = getQueryParams(program=self.program)
        session = self.config.get_session()
        response = session.get(url, params=query_param)
        return response.json()

    # Get reports of all status.
    def getAllReports(self):
        url = self.urls["reports"]
        query_params = getQueryParams(program=self.config.program)
        return self.get_call(url, query_params)

    # Get all closed reports.
    def getAllReports(self):
        url = self.urls["reports"]
        query_params = getQueryParams(program=self.config.program)
        return self.get_call(url, query_params)

    # Get reports of all status.
    def getReports(self, byUser: str = None):
        url = self.urls["reports"]
        query_params = getQueryParams(program=self.config.program)
        return self.get_call(url, query_params)


def getQueryParams(sort: str = None, state: str = None, **kwargs):
    query = {"filter": {}}
    for key, val in kwargs.items():
        query["filter"][key] = val
    if sort:
        query["sort"] = sort

    return encode_params(query)


def encode_params(obj, keys=()):
    if isinstance(obj, dict):
        # When you have nested dict:
        #   Ex: key[bar]=1&key[baz]=2
        params = []
        for key, value in obj.items():
            params.append(encode_params(value, keys + (key,)))
        return "&".join(params)
    elif isinstance(obj, (list, tuple)):
        # When you have multiple values for a property.
        #   Ex: key[foo][]=1&key[foo][]=2
        params = []
        for value in obj:
            params.append(encode_params(value, keys + ("",)))
        return "&".join(params)
    else:
        # This is the last level, where the data is formatted as required by the request.
        # All the upper level keys needs to be nested, equating the value.
        #   Ex: `obj` is just a value, key=1
        #   All keys but top-level keys should be in brackets, i.e,
        #       `key[foo]=1`, not `[key][foo]=1`.
        encoded_keys = ""
        for depth, key in enumerate(keys):
            # All keys but top-level keys should be in brackets, i.e.
            # `key[foo]=1`, not `[key][foo]=1`
            if depth == 0:
                encoded_keys += key
            else:
                encoded_keys += "[" + key + "]"
        return encoded_keys + "=" + obj
