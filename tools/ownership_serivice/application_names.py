from util.file_util import write_to_file
from util.httpcaller import get_session

session = get_session()
session.verify = False


def get_application_names():
    url = "https://kube-ownership.service.intraiad1.consul.csnzoo.com/Objects?includeUnclaimed=false&offset=0&limit=10666"

    payload = {}
    headers = {
        'Accept': 'application/json'
    }

    response = session.get(url, headers=headers, data=payload)
    json_response = response.json()
    app_names = []
    for app_name in json_response["payload"]["items"]:
        app_names.append(app_name)
    write_to_file("application_names.txt", app_names)


if __name__ == "__main__":
    get_application_names()
