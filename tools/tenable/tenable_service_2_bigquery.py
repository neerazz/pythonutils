import logging
import time
from datetime import datetime, timedelta
from typing import List

from tools.bigquery.bigquery_json_util import getSchema
from tools.bigquery.bigquery_service import BigQueryClient
from tools.tenable.tenable_client import TenableClient

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

tenableTables = {
    'scanners': "tenable_scanners",
    'agent_groups': "tenable_agent_groups",
    'agents': "tenable_agents",
    'assets': "tenable_asserts",
    'asset_vulnerabilities': "tenable_asset_vulnerabilities",
    'asset_vulnerability_output': "tenable_asset_vulnerability_output",
}

time_format = "%Y-%m-%dT%H:%M:%S.%f"

tenable_client = TenableClient()
bqClient = BigQueryClient()


def getTime(days: int = 0, hours: int = 0):
    datetime_now = datetime.now()
    datetime_now = datetime_now - timedelta(days=days, hours=hours)
    timestamp = datetime_now.strftime(time_format)
    return "{}Z".format(timestamp[:-3])


def addAssertData(input_json: dict):
    process = 'assets'
    tableName = tenableTables[process]
    insertValues = [input_json]
    if bqClient.table_exists(tableName):
        bqClient.insertToTable(tableName, insertValues)
    else:
        assertsSchema = getSchema(insertValues[0])
        bqClient.createTable(tableName, assertsSchema)
        time.sleep(1)
        bqClient.insertToTable(tableName, insertValues)


def addAssertsData(input_json: List[dict]):
    process = 'assets'
    tableName = tenableTables[process]
    if bqClient.table_exists(tableName):
        bqClient.insertToTable(tableName, input_json)
    else:
        # TODO: Plan to through an exception.
        log.info(f"The input Table : {tableName}, not present.")


def add_asset_vulnerabilities(input_json: List[dict]):
    process = 'asset_vulnerabilities'
    tableName = tenableTables[process]
    if bqClient.table_exists(tableName):
        bqClient.insertToTable(tableName, input_json)
    else:
        assertsSchema = getSchema(input_json[0])
        bqClient.createTable(tableName, assertsSchema)
        time.sleep(1)
        bqClient.insertToTable(tableName, input_json)


def add_assets_vulnerability_by_plugin(input_json: dict):
    process = 'asset_vulnerability_by_plugin'
    tableName = tenableTables[process]
    insertValues = input_json["outputs"]
    if bqClient.table_exists(tableName):
        bqClient.insertToTable(tableName, insertValues)
    else:
        assertsSchema = getSchema(insertValues[0])
        bqClient.createTable(tableName, assertsSchema)
        time.sleep(1)
        bqClient.insertToTable(tableName, insertValues)


def add_assert_vulnerability_outputs(input_json: List[dict]):
    process = 'asset_vulnerability_output'
    tableName = tenableTables[process]
    if bqClient.table_exists(tableName):
        bqClient.insertToTable(tableName, input_json)
    else:
        assertsSchema = getSchema(input_json[0])
        bqClient.createTable(tableName, assertsSchema)
        time.sleep(1)
        bqClient.insertToTable(tableName, input_json)


def add_agent_groups(agentGroups):
    process = "agent_groups"
    tableName = tenableTables[process]
    if bqClient.table_exists(tableName):
        bqClient.insertToTable(tableName, agentGroups)
    else:
        schema = getSchema(agentGroups[0])
        bqClient.createTable(tableName, schema)
        time.sleep(1)
        bqClient.insertToTable(tableName, agentGroups)


def add_agents(agents):
    process = "agents"
    tableName = tenableTables[process]
    if bqClient.table_exists(tableName):
        bqClient.insertToTable(tableName, agents)
    else:
        schema = getSchema(agents[0])
        bqClient.createTable(tableName, schema)
        time.sleep(1)
        bqClient.insertToTable(tableName, agents)


def process_agents_from_scanners(scannerId):
    res = tenable_client.get_agent_group(scannerId)
    if "groups" in res:
        agentGroup = res['groups']
        add_agent_groups(agentGroup)
        for group in agentGroup:
            process_agents_from_scanner_group(scannerId, group["id"])


def process_agents_from_scanner_group(scannerId: int, agentGroupId: int, offset: int = 0):
    res = tenable_client.get_agents(scannerId, agentGroupId, offset=offset)
    agents = res["agents"] if "agents" in res else []
    total = res["pagination"]["total"] if "pagination" in res else 0
    next_start = offset + len(agents)
    if agents:
        add_agents(agents)
    if next_start < total:
        process_agents_from_scanner_group(scannerId, agentGroupId, next_start)


def process_assert_vulnerability(assert_id: str, assert_vul: dict):
    if 'plugin_id' in assert_vul:
        plugin_id = assert_vul['plugin_id']
        assert_vul = tenable_client.get_asset_vulnerability_by_plugin(assert_id, plugin_id)
        if "outputs" in assert_vul:
            asserts_outputs = assert_vul["outputs"]
            add_assert_vulnerability_outputs(asserts_outputs)


def process_asset_vulnerabilities(assert_id: str, vulnerabilities=None):
    if vulnerabilities is None:
        resp_json = tenable_client.get_asset_vulnerabilities(assert_id)
        vulnerabilities = resp_json["vulnerabilities"]
    if vulnerabilities:
        add_asset_vulnerabilities(vulnerabilities)
        for vul in vulnerabilities:
            process_assert_vulnerability(assert_id, vul)
    return vulnerabilities


def process_assert(tenable_assert):
    assert_id = tenable_assert["id"]
    res = tenable_client.get_asset_vulnerabilities(assert_id)
    if "vulnerabilities" in res:
        vulnerabilities = res["vulnerabilities"]
        process_asset_vulnerabilities(assert_id, vulnerabilities)


def process_daily_asserts(days: int = 0, hours: int = 1):
    query = {
        "date_range": 0,
        "filter.0.filter": "first_scan_time",
        "filter.0.quality": "date-gt",
        "filter.0.value": getTime(days=days, hours=hours)
    }
    res = tenable_client.get_asserts(query)
    if "assets" in res:
        tenable_asserts = res["assets"]
        addAssertsData(tenable_asserts)
        for a in tenable_asserts:
            process_assert(a)
    else:
        log.error(f"Unexpected Response for Asserts : {res}")


def start_process_and_to_bigquery():
    assert_ids = set()
    all_vul = tenable_client.get_vulnerabilities_by_plugin()
    # add_assets_vulnerabilities_by_plugin(all_vul)
    for v in all_vul["vulnerabilities"]:
        plugin_id = v["plugin_id"]
        vulnerabilities_by_plugin = tenable_client.get_asset_vulnerability_by_plugin(plugin_id)
        add_assets_vulnerability_by_plugin(vulnerabilities_by_plugin)
        for a in vulnerabilities_by_plugin["outputs"]:
            assert_ids.add(a["host_id"])
        time.sleep(0.1)

    time.sleep(1)

    for assert_id in assert_ids:
        assert_details = tenable_client.get_assert(assert_id)
        addAssertData(assert_details)
        time.sleep(0.1)


def start_agents_flow():
    res = tenable_client.get_scanners()
    if "scanners" in res and len(res["scanners"]) > 0:
        scanner_id = res["scanners"][0]['id']
        process_agents_from_scanners(scanner_id)


if __name__ == '__main__':
    print('This is a sample Script, with all the helpful implementations, related to Tenable.')

    # assert_response_file_name = "tenable/responses/Get_Asserts_response.json"
    # scans_response_file_name = "tenable/responses/List_scans_response.json"
    # vulnerabilities_response_file_name = "tenable/responses/get_vulnerabilities_by_plugin.json"

    # This function makes an API call to get all the scans.
    # scans = get_scans()
    # print(scans)

    # This function provides a mock API metadata JSON, to get all the scans.
    # scans_response_file = open(scans_response_file_name)
    # print(get_scans_from_json(json.load(scans_response_file)))

    # This function makes an API call to get all the asserts.
    # print(get_asserts())

    # This function provides a mock API metadata JSON, to get all the asserts.
    # assert_response_file = open(assert_response_file_name)
    # response_object = get_asserts_from_json(json.load(assert_response_file))
    # print(response_object)

    # start_process_and_to_sheet()
    # start_process_and_to_bigquery()
    process_daily_asserts(days=7)
    # start_agents_flow()
