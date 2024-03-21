import json
import logging

logger = logging.getLogger(__name__)


def dump_jsonl(data, output_path, append=False):
    """
    Write list of objects to a JSON lines file.
    """
    mode = 'a+' if append else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        for line in data:
            json_record = json.dumps(line, ensure_ascii=False)
            f.write(json_record + '\n')
    print('Wrote {} records to {}'.format(len(data), output_path))


def load_jsonl(input_path) -> list:
    """
    Read list of objects from a JSON lines file.
    """
    data = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line.rstrip('\n|\r')))
    print('Loaded {} records from {}'.format(len(data), input_path))
    return data


def toNewlineDelimited_JSON(json_input: str):
    result_string = ""
    # json_data = bigjson.load(json_input)
    for record in json_input:
        # Converts json to a Python dict
        # dict_record = record.to_python()
        result_string += json.dumps(record) + "\n"
    return result_string


if __name__ == '__main__':
    logger.info("Loading Json To New Lined Delimited Json Utility.")
    assert_response_file_name = "../tools/tenable/responses/Get_Asserts_response.json"
    assert_response_file_name_o = "../tools/tenable/responses/Get_Asserts_response_o.json"
    loaded_data = load_jsonl(assert_response_file_name)
    dump_jsonl(loaded_data, assert_response_file_name_o)
    assert_response_file = open(assert_response_file_name)
    assert_response_json = json.load(assert_response_file)
    newline_delimited_json = toNewlineDelimited_JSON(assert_response_json)
    print(newline_delimited_json)
