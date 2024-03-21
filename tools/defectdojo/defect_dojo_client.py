from tools.defectdojo.defect_dojo_config import DefectDojoConfig


class DefectDojoClientV2:
    base_url = "https://defectdojo.service.csnzoo.com/api/v2"
    limit = 200
    urls = {
        "": base_url,
        "products": base_url + "/products",
        "product": base_url + "/products/{}",
        "findings": base_url + "/findings",
        "finding": base_url + "/findings/{}",
        "endpoints": base_url + "/endpoints",
        "endpoint": base_url + "/endpoints/{}"
    }

    def __init__(self):
        self.config = DefectDojoConfig()

    def make_request(self, url):
        session = self.config.get_session()
        response = session.get(url)
        return response.json()

    def get_call(self, url: str, query_param: dict = None):
        session = self.config.get_session()
        response = session.get(url, params=query_param)
        return response.json()

    # Get all the products
    def getAllProducts(self, limit: int = None, recursiveCalls: bool = True):
        if limit is None:
            limit = self.limit

        url = self.urls["products"]
        query_params = {"limit": limit}
        products = []

        def check_next(res):
            next_url = res["next"]
            results = res["results"]
            if results:
                products.extend(results)
            if next_url:
                check_next(self.make_request(next_url))

        response_json = self.get_call(url, query_params)
        if recursiveCalls:
            check_next(response_json)
        else:
            products.extend(response_json["results"])
        return products

    def getProduct(self, productId: int):
        url = self.urls["product"].format(productId)
        return self.get_call(url)

    # Get all the findings
    def getFindings(self, limit: int = None, recursiveCalls: bool = True):
        if limit is None:
            limit = self.limit

        url = self.urls["findings"]
        query_params = {"limit": limit}
        findings = []

        def check_next(res):
            next_url = res["next"]
            results = res["results"]
            if results:
                findings.extend(results)
            if next_url:
                check_next(self.make_request(next_url))

        response_json = self.get_call(url, query_params)
        if recursiveCalls:
            check_next(response_json)
        else:
            findings.extend(response_json["results"])
        return findings

    def getFinding(self, findingId: int):
        url = self.urls["findings"].format(findingId)
        return self.get_call(url)

    # Get all the Endpoints
    def getEndpoints(self, limit: int = None, recursiveCalls: bool = True):
        if limit is None:
            limit = self.limit

        url = self.urls["endpoints"]
        query_params = {"limit": limit}
        findings = []

        def check_next(res):
            next_url = res["next"]
            results = res["results"]
            if results:
                findings.extend(results)
            if next_url:
                check_next(self.make_request(next_url))

        response_json = self.get_call(url, query_params)
        if recursiveCalls:
            check_next(response_json)
        else:
            findings.extend(response_json["results"])
        return findings

    def getEndpoint(self, endpointId: int):
        url = self.urls["endpoint"].format(endpointId)
        return self.get_call(url)
