import logging

from util.credentialsdetails import get_secret
from util.httpcaller import get_session

log = logging.getLogger(__name__)


class DefectDojoConfig:
    retries_for_token = 2

    def __init__(self):
        self.access_token = get_secret("defect_dojo_access_token")

    def get_session(self):
        log.info('Generating DefectDojo Session')
        session = get_session(self.get_header())
        session.verify = False
        return session

    def get_header(self):
        return {'Authorization': "Token {}".format(self.access_token)}
