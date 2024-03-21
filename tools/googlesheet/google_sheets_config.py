import logging
import time
from typing import Tuple

import jwt as jwt

from util.credentialsdetails import get_oauth_access_token, get_config, get_secret
from util.httpcaller import get_session

log = logging.getLogger(__name__)


class GoogleSheetConfig:
    grant_type = "urn:ietf:params:oauth:grant-type:jwt-bearer"
    scope = 'https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/spreadsheets'
    jwt_header = {"alg": "RS256", "typ": "JWT"}
    retries_for_token = 2

    def __init__(self):
        self.access_token_url = get_config("google_access_token_url")
        self.service_account = get_config("google_service_account_sheets")
        self.communication_email = get_config("email_address")
        self.private_key_secret = get_secret("google_private_key")

    def get_session(self):
        header = self.get_header_token()
        return get_session(header)

    def get_header_token(self, retry=0):
        if self.retries_for_token > 2:
            return {}
        access_token, expiry_time = self.access_token()
        log.info(f"Access Token : {access_token}")
        log.info(f"Expiry Time : {expiry_time}")
        cur_time = time.time()
        if isinstance(expiry_time, float) and (expiry_time - cur_time) > 60:
            return {'Authorization': 'Bearer %s' % access_token}
        else:
            return self.get_header_token(retry + 1)

    # https://developers.google.com/identity/protocols/oauth2/service-account#httprest
    def access_token(self) -> Tuple[str, int]:
        log.info("Retrieving Access token for Google Sheet")
        data = {'grant_type': self.grant_type,
                'assertion': self.signed_jwt()}
        return get_oauth_access_token(self.access_token_url, data=data)

    def signed_jwt(self):
        log.info("Getting the signed token for Google Sheet")
        jwt_claim_set = self.get_jwt_claim_set()
        private_secret = bytes(self.get_private_key().replace('\\n', '\n'), "utf-8")
        jwt_encode = jwt.encode(jwt_claim_set, private_secret, headers=self.jwt_header, algorithm='RS256')
        return jwt_encode

    def get_jwt_claim_set(self):
        log.info("Creating jwt_claim_set for Google Sheet")
        iat = int(time.time())
        exp = iat + 3600
        return {
            'iss': self.service_account,
            'scope': self.scope,
            'sub': self.communication_email,
            'aud': self.access_token_url,
            'iat': iat,
            'exp': exp
        }

    def get_private_key(self) -> str:
        log.info(f"Retrieving the private key for Google Sheet.")
        if self.private_key_secret is None:
            return ""
        elif self.private_key_secret.startswith("-" * 5):
            return self.private_key_secret
        else:
            private_key_header = '-' * 5 + "BEGIN PRIVATE KEY" + '-' * 5
            private_key_footer = '-' * 5 + "END PRIVATE KEY" + '-' * 5
            return f"{private_key_header}\n{self.private_key_secret}\n{private_key_footer}"
