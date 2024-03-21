import logging
from typing import Tuple

from util.credentialsdetails import get_config, get_secret, get_oauth_access_token

logger = logging.getLogger(__name__)


def crowdstrike_access_token() -> Tuple[str, str]:
    logger.info('Generating Crowdstrike access token')
    client_id = get_config('crowdstrike_client_id')
    client_secret = get_secret('crowdstrike_secret_key')
    headers = {'Content-Type': 'application/x-www-form-urlencoded', "accept": "application/json"}
    data = {'client_id': client_id, 'client_secret': client_secret}
    return get_oauth_access_token(get_config("crowdstrike_access_token_url"), headers, data)
