import logging

from tools.tenable.tenable_config import TenableConfig

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class TenableClient:
    base_url = "https://cloud.tenable.com"
    urls = {
        "": base_url,
        "scanners": base_url + "/scanners",
        "agent_groups": base_url + "/scanners/{}/agent-groups",
        "agents": base_url + "/scanners/{}/agent-groups/{}/agents",
        "scans": base_url + "/scans",
        "assets": base_url + "/workbenches/assets",
        "assets_vulnerabilities": base_url + "/workbenches/assets/vulnerabilities",
        "asset_vulnerabilities": base_url + "/workbenches/assets/{}/vulnerabilities",
        "asset_vulnerability": base_url + "/workbenches/assets/{}/vulnerabilities/{}/outputs",
        "asset": base_url + "/assets/{}",
        "vulnerabilities": base_url + "/workbenches/vulnerabilities",
        "asset_vulnerability_by_plugin": base_url + "/private/workbenches/vulnerabilities/{}/outputs/truncate"
    }

    def __init__(self, dateRange: int = 0):
        self.tenableConfig = TenableConfig()
        self.data_range = dateRange

    def _get_session(self):
        return self.tenableConfig.get_session()

    def _get_call(self, url: str, call_parm: dict = None):
        call_parm = {} if call_parm is None else call_parm
        session = self._get_session()
        response = session.get(url, params=call_parm)
        return response.json()

    # Get list of scanners
    def get_scanners(self):
        log.info("Making an API call to get teh list of Scanners")
        process = "scanners"
        url = self.urls[process]
        response_json = self._get_call(url)
        return response_json

    # Get list of agents in scanner. YOu can provide any random scanner ID.
    def get_agent_group(self, scannerId: int):
        log.info("Making an API call to get teh list of Scanners")
        process = "agent_groups"
        url = self.urls[process].format(scannerId)
        response_json = self._get_call(url)
        return response_json

    # Get list of agents in scanner. You can provide any random scanner ID.
    def get_agents(self, scannerId: int, agentGroup: int, limit: int = 1000, offset: int = 0):
        log.info("Making an API call to get the list of Scanners")
        process = "agents"
        query_parm = {"limit": limit, "offset": offset}
        url = self.urls[process].format(scannerId, agentGroup)
        response_json = self._get_call(url, query_parm)
        return response_json

    # Get list of asserts
    def get_asserts(self, query_parm: dict = None):
        log.info("Making an asserts endpoint call.")
        if query_parm is None:
            query_parm = {"data_range": self.data_range}
        process = "assets"
        url = self.urls[process]
        response_json = self._get_call(url, query_parm)
        return response_json

    # Get assert details
    def get_assert(self, assertId: str):
        log.info("Making an assertDetail endpoint call.")
        process = "asset"
        url = self.urls[process].format(assertId)
        response_json = self._get_call(url)
        return response_json

    # Get assert vulnerability
    def get_asset_vulnerabilities(self, assertId: str):
        log.info("Making an assertDetail endpoint call.")
        process = "asset_vulnerabilities"
        url = self.urls[process].format(assertId)
        response_json = self._get_call(url)
        return response_json

    # Get list of scans
    def get_scans(self):
        log.info("Making a Scan endpoint call.")
        process = "scans"
        url = self.urls[process]
        response_json = self._get_call(url)
        return response_json

    # Get list of vulnerabilities
    def get_vulnerabilities_by_plugin(self):
        log.info("Making a Scan endpoint call.")
        query_params = {"data_range": self.data_range}
        process = "vulnerabilities"
        url = self.urls[process]
        response_json = self._get_call(url, query_params)
        return response_json

    # Get vulnerabilities by plugin
    def get_asset_vulnerability_by_plugin(self, assertId: str, pluginId: str):
        process = "asset_vulnerability"
        log.info("Making a Scan endpoint call.")
        query_params = {"data_range": self.data_range}
        url = self.urls[process].format(assertId, pluginId)
        response_json = self._get_call(url, query_params)
        return response_json


if __name__ == '__main__':
    print('This is a sample Script, with all the helpful implementations, related to Tenable.')
