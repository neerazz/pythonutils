import json
import logging
import re
from datetime import datetime

from google.cloud.bigquery import SchemaField

from util.datetime_util import getTimeStamp

log = logging.getLogger(__name__)


def createSchema(fieldName: str, fieldType: str, properties: dict = None) -> SchemaField:
    if "fields" in properties and "mode" in properties:
        return SchemaField(fieldName, fieldType, mode=properties["mode"], fields=properties["fields"])
    elif "mode" in properties:
        return SchemaField(fieldName, fieldType, mode=properties["mode"])
    else:
        return SchemaField(fieldName, fieldType)


def isTimeStamp(inputValue) -> bool:
    try:
        if isinstance(inputValue, str):
            return isinstance(getTimeStamp(inputValue), datetime)
    except ValueError:
        return False


regex_pattern = "^[A-Za-z0-9_]*$"


# Fields must contain only letters, numbers, and underscores,
#   start with a letter or underscore, and be at most 300 characters long
def validFieldName(fieldName: str) -> str:
    if re.match(regex_pattern, fieldName):
        if fieldName[0].isalpha():
            return fieldName
        else:
            return "_{}".format(fieldName)
    else:
        # TODO create a function that will only include valid characters.
        return "_{}".format(fieldName)


def validateInputData(insertData):
    if isinstance(insertData, (list, set, tuple)):
        valid_list = []
        for eachInput in insertData:
            valid_list.append(validateInputData(eachInput))
        return valid_list
    elif isinstance(insertData, dict):
        valid_dict = dict()
        for key, value in insertData.items():
            valid_dict[validFieldName(key)] = validateInputData(value)
        return valid_dict
    else:
        return insertData


def getSchema(json_data):
    schema = []
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            fieldType = "STRING"
            properties = dict()
            if isinstance(value, bool):
                # TODO: Handle the case where the value is boolean
                fieldType = "BOOLEAN"
            elif isinstance(value, int):
                fieldType = "INTEGER"
            elif isinstance(value, float):
                fieldType = "FLOAT"
            elif isinstance(value, (list, set, tuple)):
                properties["mode"] = "REPEATED"
                if len(value) == 0 or isinstance(value[0], str):
                    log.info(f"Ignoring the empty list for the key : {key}")
                elif isinstance(value[0], int):
                    fieldType = "INTEGER"
                elif isinstance(value[0], float):
                    fieldType = 'FLOAT'
                else:
                    fieldType = "RECORD"
                    properties["fields"] = getSchema(value[0])
            elif isinstance(value, dict):
                fieldType = "RECORD"
                properties["mode"] = "NULLABLE"
                properties["fields"] = getSchema(value)
            elif isTimeStamp(value):
                fieldType = "STRING"
            # Validate The key (Field Name)
            schema.append(createSchema(validFieldName(key), fieldType, properties))
    elif isinstance(json_data, str):
        schema.append(createSchema("str", "STRING"))
    else:
        log.info(f"Type of json data is {type(json_data)}. It is Invalid.")
    return schema


if __name__ == '__main__':
    log.info("Loading BigQuery Persistence Utility.")
    # file_name = "../tenable/responses/Get_Asserts_response.json"
    # assert_response_file = open(file_name)
    # input_json = json.load(assert_response_file)
    # schemas = getSchema(input_json)
    # print(schemas)
    file_name = "../hackerone/responses/all_vulnerabilities_report.json"
    assert_response_file = open(file_name)
    response_json = json.load(assert_response_file)
    validate_input_data = validateInputData(response_json)
    print(validate_input_data)
