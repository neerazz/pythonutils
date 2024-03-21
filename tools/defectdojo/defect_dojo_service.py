import json
import logging
from typing import List

from tools.bigquery.bigquery_json_util import getSchema
from tools.bigquery.bigquery_service import BigQueryClient
from tools.defectdojo.defect_dojo_client import DefectDojoClientV2

log = logging.getLogger(__name__)

bq_client = BigQueryClient()
dd_client = DefectDojoClientV2()

tables = {
    "products": "defect_dojo_products",
    "findings": "defect_dojo_findings"
}


def create_product_table(product):
    tableName = tables["products"]
    product_schema = getSchema(product)
    bq_client.createTable(tableName, product_schema)


def select_product(productId):
    None


def process_product(productId):
    None


def process_products(productIds: List = None, products: List = None):
    products = dd_client.getAllProducts()
    save_products(products)
    for product in products:
        process_findings(findingsIds=product["findings_list"])


def save_products(products: List):
    tableName = tables["products"]
    bq_client.insertToTable(tableName, products)


def create_finding_table(finding):
    tableName = tables["findings"]
    finding_schema = getSchema(finding)
    bq_client.createTable(tableName, finding_schema)


def select_finding(finding):
    None


def save_findings(findings):
    log.info(f"Saving {len(findings)} findings.")
    tableName = tables["findings"]
    bq_client.insertToTable(tableName, findings)


def process_findings(findingsIds: List = None):
    log.info("Processing Findings")
    if findingsIds:
        # Make an API call to get individual the findings
        for fId in findingsIds:
            finding = dd_client.getFinding(fId)
            save_findings([finding])
    else:
        # Make an API call to get all the findings
        findings = dd_client.getFindings()
        save_findings(findings)


if __name__ == '__main__':
    print('This is a sample Script, with all the helpful implementations, related to Defectdojo.')
    #
    # Steps to create a product Table
    #
    product_file_name = "responses/product.json"
    product_file = open(product_file_name)
    product_json = json.load(product_file)
    create_product_table(product_json)
    #

    #
    # Steps to create a finding's table
    #
    finding_file_name = "responses/finding.json"
    finding_file = open(finding_file_name)
    finding_file_json = json.load(finding_file)
    create_finding_table(finding_file_json)
    # save_findings([finding_file_json])

    #
    # Starting the process from products
    #
    process_products()
    #

    #
    # Starting the process from findings
    #
    process_findings()
    #
