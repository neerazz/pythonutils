import json
import logging
import time

from util.httpcaller import get_session

logger = logging.getLogger(__name__)

wf_config = {
    "google_access_token_url": 'https://www.googleapis.com/oauth2/v4/token',
    "crowdstrike_access_token_url": "https://api.crowdstrike.com/oauth2/token",
    "email_address": "secopsteamdrive@wayfair.com",
    "project_id": "wf-us-forensics-sandbox",
    "bigquery_dataset_id": "security_datastore",
    "hacker_one_user_name": "nbeshane",
    "google_service_account_sheets": "secopsdrivesheet@secopsgsuite.iam.gserviceaccount.com",
    "google_service_account_bigquery": "security-automation@wf-us-forensics-sandbox.iam.gserviceaccount.com",
}

wf_secrets = {
    "crowdstrike_client_id": "",
    "crowdstrike_secret_key": "",
    "defect_dojo_access_token": "8ce81784ba865913b2cabe5543a851d756fad256",
    "hacker_one_api_token": "kHrJp+9NSASl99MBIMPqlaRn2riG3vp3hlsGfM6A9jg=",
    "google_service_automation_json": "/Users/nb336n/Documents/secrets/inst-vulnerability-mnt-svc-prod.json",
    "tenable_access_key": "b1db1d661702712c706f1ce162f63b2273fb59a224026df91b8efbadb81b142b",
    "tenable_secret_key": "d8566b9073db43f71c0da9c1f185a62438358208889f2a0f61035df8ccf0c580",
    "google_private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC/68464uWKgpiQ\nD+8W+YmjtgYxQx0leseaCDTQ8/7topQd0+iYXAzYTDzfs55BG5PVVKbhKQZLQnx3\n3T+Lib08+qo4dzdhC+W0ucL8EvQHFtZae5Uh9ofGZj3qiicGc3JaLutpnEI1eDyz\nSSKWBSTk4EcxUclPbYpIiktQVwFmBgC/Yj2VE8CytX1skRtRW9tmpHvEkflcPlsL\nAt2jE7zvSmckklMBIyR5hQAjx9IJgNLtaKAiEA+HJ6yGooM546IsM3My7P1Z83WT\n66R1ssfouDgg89qjvpAvkr7juT4m2GBi0/SPaXYzbd8IV8wNyRV9ALg7XClMnMnn\n8wik6QUDAgMBAAECggEABmnM1G7smLpQes/tf2kLTmswvciuWqhFr0IC8dCVfj9m\nj7CbHyxESZ4Skq8f5LEVOZXAldmXGkC4hBDipLkPl9AQjB5/vUB2hpmGiIHhobMD\nqrZif2YLl3enLgU71J1a/uR+fWL5W2wPKzaQb07wsq1D88P15C+W5WGprp+Zrl0K\nLGzIBllSvD9Uki437AnZdAgdud3hdiXvWnuB0tV6qmjpEeHi4lrzvFz6Iq9nBjmK\noheX8woJQ2oJzhbNofTk9pGZB+8G1O+NBN1yX5+tIcVqc9VXjgOvhAcgrbg+92YY\nhUapOuW2ujbmGuCU/qCwb1EMm6/PjOupvRsPR5WMYQKBgQDhWpD0xJtSvgFoNsAi\n8q19TUDKuZR+Y3DtvM6BqKZkZeOUhTfcpkx/UgpSC9Vlwb427Y522xnStFUawGJ8\nmM+VPHoCCnQ5iCEgbvPZzXkS43ZWyjaqMoNi5A7n65kKv2tKPLzEZ6/9X1KzsQy/\nnWJLhwh6PRhiszSH+nnIKcxdiQKBgQDaBVHQ+1SIbKFIs4DErBeh6YNIEsBOUItS\nmsl7RCcIl/I47gdglYnzjcu/Mx7ghHq8TiUz9SMXA4hQxBMrtoaABhpHIXOINSM6\nrXJi9ooK4tOBVsNW2+2dFH/IYA3ijeCWkqouzda9Vl7uWRVKuDZFKt3VK1ZVl9zX\ndp1xvD4XKwKBgHtcvKWBSxXMdbC66As5lcdWFvXjCWr2vMcn6FQKIqwrKp4PHzlm\nv9Gi84tedv8xRBOFj8t4vXYeycfPMRrL/DbR2GhtmJo17wx2MH82f+TbJ9jy8WHS\nLSJhfddvnWPIzc7h2OQbbrfhCsDbVwM+AKUf0oA4GbVOLJ+Tej8cwochAoGAV4WN\nK6zJaZ7aPDo7Njizn/8DAbrtUkMJOxcCTSa12MBOr8X2VjKR16ETquTVv2HPd6qT\nSsFc3c9AONQNsh2q7tgEUou+Om7CfrrEUbARCH+4UpLHBiZxw/5HsePFjy5Pe4LT\nKMjfLNDweRRv9LfwqWGk/f9QwDmfoStv1wmvj1MCgYBLSIkTLTYyPv0+u7QlyXpz\nPezvKhnaBKfbRwq/esAXQSstHR1hfTe8GA8qmhgn5RAgkGtUs5x9Pl60ZdmCmn/B\n3RQWN18RtGF1VM1InxyUFEZS+fYtT1Vungcp/9SUvqQsOznrYgYX1iAzLRQ5efI0\npYdpshw9EmCN1/JDWAFBQA==\n-----END PRIVATE KEY-----\n"
}


def get_config(key: str) -> str:
    return wf_config.get(key)


def get_secret(key: str) -> str:
    return wf_secrets.get(key)


def get_oauth_access_token(url: str, headers: dict = None, data: dict = None, keyName: str = "access_token"):
    logger.info(f"Generating access token from : {url}")
    session = get_session(headers)
    response = session.post(url, data=json.dumps(data))
    response_json = response.json()
    access_token, expiry = None, None
    if response.ok:
        access_token = response_json[keyName]
        expiry = time.time() + response_json['expires_in']
    elif response.status_code == 429:
        logger.error('Too many requests. Sleeping %s' % response_json['error_description'])
    else:
        logger.error('Failed to generate access token')
        logger.error("%d:%s" % (response.status_code, response.text))
    return access_token, expiry
