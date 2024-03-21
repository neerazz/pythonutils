# Generate session with max of 3 retries and interval of 1 second
import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 60  # seconds
DEFAULT_RETRY = 3  # times
'''
BACKOFF_FACTOR      It allows you to change how long the processes will sleep between failed requests. The algorithm is as follows
                    If the backoff factor is set to:
                            1 second the successive sleeps will be 0.5, 1, 2, 4, 8, 16, 32, 64, 128, 256
'''
DEFAULT_BACKOFF_FACTOR = 2  # times


def get_header():
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


def retry_strategy(**kwargs):
    retries = kwargs["total"] if "total" in kwargs else DEFAULT_RETRY
    backoff_factor = kwargs["backoff_factor"] if "backoff_factor" in kwargs else DEFAULT_BACKOFF_FACTOR
    return Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )


def get_session(headers: dict = None, **kwargs):
    session = requests.Session()
    retries = retry_strategy(**kwargs)
    properties = TimeoutHTTPAdapter(max_retries=retries)
    for key, value in get_header().items():
        session.headers.setdefault(key, value)
    if headers:
        for key, value in headers.items():
            session.headers.setdefault(key, value)

    session.mount('http://', properties)
    session.mount('https://', properties)
    return session


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)
