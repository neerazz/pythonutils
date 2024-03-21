from google.cloud import bigquery
from pandas import Timestamp

from tools.bigquery.bigquery_service import BigQueryClient
from util.file_util import read_from_xls

project_name = "wf-gcp-us-ae-sec-prod"
data_set = "vulnerability_management"
table_name = "simon_badging"
bq_client = BigQueryClient(project_name, data_set)


class BadgeFile:
    credential = ""
    name = ""
    company = ""
    dataTime = None
    location = ""

    def __int__(self, credential: str, name: str, company: str, dataTime: Timestamp, location: str):
        self.credential = credential
        self.name = name
        self.company = company
        self.dataTime = dataTime
        self.location = location


def createTable():
    schema = [
        bigquery.SchemaField("badgeId", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("name", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("company", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("timestamp", "TIMESTAMP"),
        bigquery.SchemaField("location", "STRING"),
    ]
    bq_client.createTable(table_name, schema)


def read_badging_file(file_name: str):
    name_label = ["badgeId", "name", "company", "timestamp", "location"]
    dataFrame = read_from_xls(file_name, names=name_label, skip_rows=[0])
    bq_row = []
    for row in dataFrame.to_dict(orient="records"):
        row_ts = row["timestamp"]
        row["timestamp"] = str(row_ts)
        bq_row.append(row)
    bq_client.insertToTable(table_name, bq_row)


if __name__ == '__main__':
    print('This is a sample project to read Lionel Badging file sample Data.')
    file_name = "/Users/nb336n/Downloads/Wayfair_Badge_Report_9.12_to_9.22.xlsx"
    # createTable()
    read_badging_file(file_name)
