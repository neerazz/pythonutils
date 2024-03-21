import json
from typing import List


def list_to_string(input_list):
    return "\n".join(input_list)


def process(json_data: dict):
    fields = {}
    for key, value in json_data.items():
        try:
            val_type = None
            if value is None or isinstance(value, str):
                val_type = "str"
            elif isinstance(value, int):
                val_type = "int"
            elif isinstance(value, list):
                if len(value) > 0:
                    first_val = value[0]
                    if isinstance(first_val, str):
                        val_type = "List"
                    else:
                        val_type = [process(first_val)]
                else:
                    val_type = []
            elif isinstance(value, dict):
                val_type = process(value)
            else:
                print(f"Key : {key}, and Value is : {value}")
                print(f"Type of value is {type(value)}")
                val_type = process(value)
            fields[key] = val_type
        except Exception as error:
            print(f"Error occurred while processing, key : {key} and value : {value}")
            print(f"Error Details: \n {error}")
    return fields


def filler():
    return " " * 5


def string_format(fields, spacing=filler()):
    strings = []
    for key, value in fields.items():
        if isinstance(value, dict):
            nested_value = string_format(value, spacing + filler())
            strings.append(spacing + key + ":")
            strings.append("\n".join(nested_value))
        elif isinstance(value, list):
            if len(value) > 0 and isinstance(value[0], dict):
                strings.append(spacing + key + ":list")
                nested_value = string_format(value[0], spacing + filler())
                strings.append("\n".join(nested_value))
            else:
                strings.append(spacing + key + ":list")
        elif isinstance(value, str):
            strings.append(spacing + key + ":" + value)
        else:
            print(f"Key : {key}, and Value is : {value}")
            print(f"Type of value is {type(value)}")
    return strings


def main(input_file, output_file):
    names = process(json.load(input_file))
    string_popo = string_format(names)
    for name in string_popo:
        print(name)


if __name__ == '__main__':
    input_file = open("../../tools/tenable/responses/List_assert_response.json")
    output_file = open("model.py")
    main(input_file, output_file)
