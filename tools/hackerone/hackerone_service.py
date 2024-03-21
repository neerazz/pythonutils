import json
import logging
from typing import List

from tools.bigquery.bigquery_json_util import getSchema
from tools.bigquery.bigquery_service import BigQueryClient
from tools.hackerone.hackerone_client import HackerOneClient

base_url = "https://api.hackerone.com/v1"
log = logging.getLogger(__name__)

ho_client = HackerOneClient()
bq_client = BigQueryClient()

hackerOneTables = {
    "reports": "hacker_one_reports"
}


def create_tables(input_json):
    reports_schema = getSchema(input_json)
    bq_client.createTable(hackerOneTables["reports"], reports_schema)


def getLastPage(reports_json):
    split = reports_json["links"]["last"].split("=")
    return int(split[-1][0])


def process_report(saveDump: bool = False):
    reports_json = ho_client.getAllReports()
    reports = reports_json["data"]

    def checkNested(parsed):
        url = parsed["links"].get('next')
        if url:
            resp = ho_client.make_request(url)
            reports.extend(resp["data"])
            checkNested(resp)

    checkNested(reports_json)

    if saveDump:
        save_all_reports(reports)
    else:
        for report in reports:
            save_or_update_report(report)


def save_all_reports(reports: List):
    bq_client.insertToTable(hackerOneTables["reports"], reports)


def save_or_update_report(report: dict):
    tableName = hackerOneTables["reports"]
    reportId = report['id']
    return save_report(report)


def save_report(report: dict):
    bq_client.insertToTable(hackerOneTables["reports"], [report])


def select_report_byID(reportId):
    reports_df = bq_client.selectFromTable(hackerOneTables["reports"], ['*'], {"id": reportId})
    return reports_df


if __name__ == '__main__':
    print('This is a sample Script, with all the helpful implementations, related to HackerOne.')
    #
    file_name = "responses/vulnerabilities_report.json"
    assert_response_file = open(file_name)
    response_json = json.load(assert_response_file)
    create_tables(response_json["data"])
    #
    # all_combined_file_name = "responses/all_vulnerabilities_only_report.json"
    # all_combined_file = open(all_combined_file_name)
    # all_combined_json = json.load(all_combined_file)
    # save_all_reports(all_combined_json)
    #
    process_report(True)
    #
    df = select_report_byID("1471704")
    print(df)
    df2 = select_report_byID("1471704sadfs")
    print(df2)
