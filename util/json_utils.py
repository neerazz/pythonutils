import json
import logging
from collections import namedtuple, OrderedDict
from typing import List, Mapping

logger = logging.getLogger(__name__)


def flat_json_fields(input_val, delimiter=".", keys=()):
    if isinstance(input_val, dict):
        flat_field = []
        for key, value in input_val.items():
            flat_field.append(flat_json_fields(value, delimiter, keys + (key,)))
        return flat_field
    elif isinstance(input_val, (list, tuple)):
        if len(input_val) > 0:
            return flat_json_fields(input_val[0], delimiter, keys)
    else:
        return delimiter.join(keys)


def toNamedtuple(obj, __class, classNames: List[str] = None) -> namedtuple:
    mapping = OrderedDict()
    className = "C"
    if isinstance(obj, (dict, Mapping)):
        if __class is None:
            if classNames is not None and len(classNames) > 0:
                className = classNames.pop()
        else:
            className = __class
        for key, value in obj.items():
            mapping[key] = toNamedtuple(value, None, classNames)
        return namedtuple_from_mapping(mapping, className)
    elif isinstance(obj, (list, set, tuple, frozenset)):
        if classNames is not None and len(classNames) > 0:
            className = classNames.pop()
        return [toNamedtuple(item, className, classNames) for item in obj]
    else:
        return obj


def namedtuple_from_mapping(mapping, name: str):
    this_namedtuple_maker = namedtuple(name, mapping.keys())
    return this_namedtuple_maker(**mapping)


def json_file_to_escaping_character(input_file):
    in_file = open(input_file)
    formatted_string = ""
    for line in in_file:
        formatted_string += line.replace('"', '\\"')
    return formatted_string


if __name__ == '__main__':
    logger.info("Loading Json Utility.")
    print(json_file_to_escaping_character(
        "/Users/nb336n/Documents/projects/security-automation/src/main/resources/avro/vms_assets.avsc"))

    assert_response_file_name = "../tools/hackerone/responses/vulnerabilities_report_required_values.json"
    assert_response_file = open(assert_response_file_name)
    assert_response_json = json.load(assert_response_file)
    # response = toNamedtuple(assert_response_json, "Asserts")
    # print(response)
    flat_json = flat_json_fields(assert_response_json)
    print("\n".join(flat_json))
