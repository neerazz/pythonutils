import json
from time import sleep

from tools.googlesheet.google_sheets_service import update_sheet_values


def format_wiz_issues(response_json):
    nodes = response_json["data"]["issues"]["nodes"]
    output_file = open("/Users/nb336n/Documents/projects/security-automation/src/test/resources/wiz_issues.csv", "w")
    row = 1
    for node in nodes:
        issue = []
        issue.append(node["id"])
        issue.append(node["control"]["id"])
        issue.append(node["control"]["name"])
        issue.append(node["description"])
        issue.append(node["control"]["resolutionRecommendation"])
        issue.append(node["createdAt"])
        issue.append(node["updatedAt"])
        issue.append(node["status"])
        issue.append(node["severity"])
        issue.append(node["entitySnapshot"]["id"])
        issue.append(node["entitySnapshot"]["type"])
        issue.append(node["entitySnapshot"]["name"])
        issue.append(node["entitySnapshot"]["cloudPlatform"])
        issue.append(node["entitySnapshot"]["subscriptionName"])
        issue.append(node["entitySnapshot"]["providerId"])
        issue.append(node["entitySnapshot"]["status"])
        issue.append(node["entitySnapshot"]["cloudProviderURL"])
        tags = node["entitySnapshot"]["subscriptionTags"]
        if tags and "application_name" in tags:
            issue.append(tags["application_name"])
        else:
            issue.append("")
        if tags and "environment" in tags:
            issue.append(tags["environment"])
        else:
            issue.append("")
        if tags and "owner_business" in tags:
            issue.append(tags["owner_business"])
        else:
            issue.append("")
        if tags and "owner_tech" in tags:
            issue.append(tags["owner_tech"])
        else:
            issue.append("")
        add_to_sheet(row, issue)
        row += 1
        sleep(1)


def add_to_sheet(row_number, cell_value):
    sheet_id = "1XoUXZ-aqkt2dMxl8PqA6Ey0JjwSHcRPT27wbvgt1o_U"
    page_id = "Wiz_Issues!"
    insertRange = f"{page_id}A{row_number}:U{row_number}"
    body = {
        "range": insertRange,
        "majorDimension": "ROWS",
        "values": [cell_value]
    }
    update_sheet_values(sheet_id, insertRange, body)


if __name__ == '__main__':
    print('This is a sample script, to format wiz issues from json to sheet.')
    response_file_name = "/Users/nb336n/Documents/projects/security-automation/src/test/resources/wiz_issues.json"
    response_file = open(response_file_name)
    response_json = json.load(response_file)
    format_wiz_issues(response_json)
