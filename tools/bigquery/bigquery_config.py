import json

from google.cloud import bigquery
from google.cloud.bigquery import Client
from google.oauth2 import service_account

from util.credentialsdetails import get_config, get_secret


def getProjectId() -> str:
    projectId = get_config("project_id")
    return projectId


def getDataSetId() -> str:
    datasetID = get_config("bigquery_dataset_id")
    return datasetID


def get_service_account_info():
    filePath = get_secret("google_service_automation_json")
    service_account_file = open(filePath)
    return json.load(service_account_file)


def get_bigquery_client_details() -> Client:
    credentials = service_account.Credentials.from_service_account_info(get_service_account_info())
    bigquery_client = bigquery.Client(project=getProjectId(), credentials=credentials)
    return bigquery_client
