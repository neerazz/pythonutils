import logging
import time
from typing import List, NamedTuple

from tools.googlesheet.google_sheets_service import get_sheet_values, update_sheet_values
from tools.tenable.model.Assert import TenableAsserts
from tools.tenable.model.Vulnerability import VulnerabilityScans
from tools.tenable.tenable_client import TenableClient

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

sheet_id = "1IsS3kkafb_sBo2FqTSmCq_cRau85JvchLZkxdVrA1G0"

sheet_tabs = {
    "metadata": "MetaData!",
    "Scans": "Scans!",
    "Assert": "Asserts!",
    "Vulnerabilities": "Vulnerabilities!",
    "Assert_Vulnerability": "Assert_Vulnerability!"
}

assert_fields = ['id',
                 'has_agent',
                 'created_at',
                 'updated_at',
                 'first_seen',
                 'last_seen',
                 'last_scan_target',
                 'last_authenticated_scan_date',
                 'last_licensed_scan_date',
                 'last_scan_id',
                 'last_schedule_id',
                 'sources',
                 'tags',
                 'interfaces',
                 'network_id',
                 'ipv4',
                 'ipv6',
                 'fqdn',
                 'mac_address',
                 'netbios_name',
                 'operating_system',
                 'system_type',
                 'tenable_uuid',
                 'hostname',
                 'agent_name',
                 'bios_uuid',
                 'aws_ec2_instance_id',
                 'aws_ec2_instance_ami_id',
                 'aws_owner_id',
                 'aws_availability_zone',
                 'aws_region',
                 'aws_vpc_id',
                 'aws_ec2_instance_group_name',
                 'aws_ec2_instance_state_name',
                 'aws_ec2_instance_type',
                 'aws_subnet_id',
                 'aws_ec2_product_code',
                 'aws_ec2_name',
                 'azure_vm_id',
                 'azure_resource_id',
                 'azure_subscription_id',
                 'azure_resource_group',
                 'azure_location',
                 'azure_type',
                 'gcp_project_id',
                 'gcp_zone',
                 'gcp_instance_id',
                 'ssh_fingerprint',
                 'mcafee_epo_guid',
                 'mcafee_epo_agent_guid',
                 'qualys_asset_id',
                 'qualys_host_id',
                 'servicenow_sysid',
                 'installed_software',
                 'bigfix_asset_id',
                 'security_protection_level',
                 'security_protections',
                 'exposure_confidence_value']

assert_vulnerabilities_fields = ['output',
                                 'output_checksum',
                                 'truncated',
                                 'port',
                                 'protocol',
                                 'service',
                                 'severity',
                                 'state',
                                 'first_found',
                                 'last_found',
                                 'host_id',
                                 'hostname',
                                 'host_ips',
                                 'host_netbios_name',
                                 'host_fqdn',
                                 'modification']

venerability_fields = ['count',
                       'plugin_family',
                       'plugin_id',
                       'plugin_name',
                       'vulnerability_state',
                       'vpr_score',
                       'accepted_count',
                       'recasted_count',
                       'counts_by_severity',
                       'cvss_base_score',
                       'cvss3_base_score',
                       'severity']


def getMetadata(metaType: str = None):
    cells = "A:B"
    sheet_resp = get_sheet_values(sheet_id, cells)
    sheet_value = {k: v for k, v in sheet_resp["values"]}
    return sheet_value[metaType] if metaType in sheet_value else sheet_value


def getBody(insertRange: str, values: List):
    body = {
        "range": insertRange,
        "majorDimension": "ROWS",
        "values": values
    }
    return body


def addAssertDataToSheet(input_nt: NamedTuple):
    process = "Assert"
    pre_count = int(getMetadata(process)) + 1
    insertRange = f"{sheet_tabs[process]}A{str(pre_count)}:BF{str(int(pre_count) + 1)}"
    values = [getFromNamedTuple(input_nt, assert_fields)]
    update_response = update_sheet_values(sheet_id, insertRange, getBody(insertRange, values))
    print(update_response)
    return update_response


def addVenerabilityAndAssertDataToSheet(input_nt: NamedTuple):
    process = "Assert_Vulnerability"
    inputFieldName = "outputs"
    pre_count = int(getMetadata(process)) + 1
    count = len(getattr(input_nt, inputFieldName))
    insertRange = f"{sheet_tabs[process]}A{str(pre_count)}:P{str(int(pre_count) + count)}"
    values = [getFromNamedTuple(v, assert_vulnerabilities_fields) for v in getattr(input_nt, inputFieldName)]
    update_response = update_sheet_values(sheet_id, insertRange, getBody(insertRange, values))
    print(update_response)
    return update_response


def addVenerabilityDataToSheet(object: NamedTuple):
    process = "Vulnerabilities"
    inputFieldName = "vulnerabilities"
    pre_count = int(getMetadata(process)) + 1
    count = len(getattr(object, inputFieldName))
    insertRange = f"{sheet_tabs[process]}A{str(pre_count)}:L{str(int(pre_count) + count)}"
    values = [getFromNamedTuple(v, venerability_fields) for v in getattr(object, inputFieldName)]
    update_response = update_sheet_values(sheet_id, insertRange, getBody(insertRange, values))
    print(update_response)
    return update_response


def getFromNamedTuple(obj, fieldNames: List[str]):
    result = []
    for field in fieldNames:
        val = ""
        try:
            val = getattr(obj, field)
        except AttributeError as error:
            logging.info(f"Field : {field} missing in Object : {obj}.")
            logging.debug(error)
        if isinstance(val, (list, set, dict, tuple)):
            result.append(str(val))
        else:
            result.append(val)
    return result


def get_asserts_from_json(response):
    return TenableAsserts(response)


def get_scans_object_from_json(response) -> VulnerabilityScans:
    return VulnerabilityScans(response)


tenable_client = TenableClient()


def start_process_and_to_sheet():
    assert_ids = set()
    all_vul = tenable_client.get_vulnerabilities_by_plugin()
    addVenerabilityDataToSheet(all_vul)
    for v in all_vul.vulnerabilities:
        plugin_id = v.plugin_id
        vulnerabilities_by_plugin = tenable_client.get_vulnerabilities_by_plugin(plugin_id)
        addVenerabilityAndAssertDataToSheet(vulnerabilities_by_plugin)
        for a in getattr(vulnerabilities_by_plugin, "outputs"):
            assert_ids.add(a.host_id)
        time.sleep(0.05)

    for assert_id in assert_ids:
        assert_details = tenable_client.get_assert(assert_id)
        addAssertDataToSheet(assert_details)


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

    start_process_and_to_sheet()
