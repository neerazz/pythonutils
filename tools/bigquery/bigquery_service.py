import logging
from typing import List, Sequence, Dict

from google.cloud import bigquery

from tools.bigquery.bigquery_config import get_bigquery_client_details, getDataSetId, getProjectId
from tools.bigquery.bigquery_json_util import validateInputData
from util.list_util import split_in_chunks

log = logging.getLogger(__name__)


class BigQueryClient:
    projectId = getProjectId()
    datasetID = getDataSetId()
    bq_client = get_bigquery_client_details()

    def __init__(self, projectId, datasetID):
        self.projectId = projectId
        self.datasetID = datasetID

    def project(self):
        print(f"Getting GCP Project")
        return self.project

    def getTableId(self, tableName: str):
        log.info(f"Getting Table id, for table Name: {tableName}")
        return "{}.{}.{}".format(self.projectId, self.datasetID, tableName)

    def datasetReference(self):
        log.info(f"Getting Dataset Reference")
        return bigquery.DatasetReference(self.projectId, self.datasetID)

    def getTables(self):
        log.info(f"Getting all the tables in {self.datasetID}")
        formattedDataSetId = f"{self.projectId}.{self.datasetID}"
        tables = self.bq_client.list_tables(formattedDataSetId)
        log.info(f"Tables contained in '{self.datasetID}':")
        tableNames = set()
        for table in tables:
            tableNames.add(table.table_id)
            log.info("{}.{}.{}".format(table.project, table.dataset_id, table.table_id))
        return tableNames

    def getTable(self, tableName: str):
        table = self.bq_client.get_table(self.getTableId(tableName))
        if table is None:
            log.info(f"Table with name :{tableName} not found.")
        else:
            self.printTableProperties(table)
        return table

    @staticmethod
    def printTableProperties(table):
        log.info("Got table '{}.{}.{}'.".format(table.project, table.dataset_id, table.table_id))
        log.info("Table schema: {}".format(table.schema))
        log.info("Table description: {}".format(table.description))
        log.info("Table has {} rows".format(table.num_rows))
        log.info("Table location: {}".format(table.location))

    def table_exists(self, tableName: str) -> bool:
        log.info(f"Checking for table : {tableName} existence.")
        return tableName in self.getTables()

    def createTable(self, tableName: str, tableSchema):
        if self.table_exists(tableName):
            log.info(f"Table : {tableName} already exists in dataset : {self.datasetID}")
        log.info("Creating table {}, with Schema : {}".format(tableName, tableSchema))
        table_ref = self.datasetReference().table(tableName)
        table = bigquery.Table(table_ref, schema=tableSchema)
        table = self.bq_client.create_table(table)
        log.info("Created table {}".format(table.full_table_id))
        return table

    def insertJsonToTable(self, tableName: str, insertData: Sequence[Dict]):
        log.info(f"Inserting {len(insertData)} rows to Table : {tableName}.")
        if self.table_exists(tableName):
            tableId = self.getTableId(tableName)
            try:
                errors = self.bq_client.insert_rows_json(tableId, insertData)
                if errors:
                    log.info("Encountered errors while inserting rows: {}".format(errors))
                else:
                    log.info(f"New rows have been added to table : {tableName}")
            except:
                log.info("Encountered errors while inserting rows: {}".format(insertData))
        else:
            log.info(f"Table : {tableName} is not present in dataset :{self.datasetID}")

    def insertToTable(self, tableName: str, insertData: List[dict]):
        log.info(f"Inserting {len(insertData)} rows to Table : {tableName}.")
        if self.table_exists(tableName):
            tableId = self.getTableId(tableName)
            validInput = validateInputData(insertData)
            chunks = split_in_chunks(validInput, 1000)

            for chunk in chunks:
                errors = self.bq_client.insert_rows_json(tableId, chunk)
                if not errors:
                    log.info(f"New rows have been added to table : {tableName}")
                else:
                    log.info("Encountered errors while inserting rows: {}".format(errors))
        else:
            log.info(f"Table : {tableName} is not present in dataset :{self.datasetID}")

    def selectFromTable(self, tableName: str, selectFields: List[str], filters: dict = None, limit: int = None):
        tableId = self.getTableId(tableName)
        query = "SELECT {} FROM {}".format(", ".join(selectFields), tableId)
        if filters is not None:
            query += ' WHERE '
            condition = []
            for key, value in filters.items():
                condition.append(f"{key}='{value}'")
            query += ' AND '.join(condition)
        if limit is not None:
            query += "LIMIT {}".format(limit)
        return self.runQuery(tableName, query)

    def runQuery(self, tableName, query):
        table = self.getTable(tableName)
        if table:
            query_job = self._submit_job(query, table.location)
            result = query_job.result()
            log.info(f"Made select query successfully. Got {result.total_rows} rows")
            return result.to_dataframe()
        else:
            log.error(f"Table with name: {tableName}, not found.")
            log.error(f"Unable to Run the query : {query}")
            raise NotImplemented(f"Table with name: {tableName}, not found.")

    def _submit_job(self, query: str, location: str, job_config: dict = None,
                    job_id_prefix: str = "Security_Automation", job_id: str = None):
        query_job = self.bq_client.query(query, location=location, job_id_prefix=job_id_prefix)
        if job_config and job_id:
            query_job = self.bq_client.query(query, location=location, job_config=job_config,
                                             job_id=job_id)
        return query_job


if __name__ == '__main__':
    log.info("Loading BigQuery Persistence Utility.")
    bqClient = BigQueryClient()
    # print(bqClient.getTables())
    # tableProperties = bqClient.getTable("tenable_asserts")
    # bqClient.printTableProperties(tableProperties)
    #
    # select_results = bqClient.selectFromTable("tenable_plugin_venerability", ["*"])
    # dataframe = select_results.to_dataframe()
    # print(dataframe)
    #
    # file_name = "../tenable/responses/Get_Asserts_response.json"
    # assert_response_file = open(file_name)
    # input_json = json.load(assert_response_file)
    # response_data = toNamedtuple(input_json, "Assert")
    # new_table = bqClient.createTable("assert", getSchema(input_json))
    # print(new_table)
    # job_config = insertConfig(response_data)
    #
    # file_name = "../hackerone/responses/all_vulnerabilities_report.json"
    # assert_response_file = open(file_name)
    # input_json = json.load(assert_response_file)
    # json_data_ = input_json["data"]
    # schema = getSchema(json_data_)
    # new_table = bqClient.createTable("hacker_one_reports", schema)
