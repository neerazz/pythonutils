import json
import logging
from typing import List

from tools.googlesheet.google_sheets_config import GoogleSheetConfig

base_url = "https://sheets.googleapis.com/v4/spreadsheets"
logger = logging.getLogger(__name__)

urls = {
    "": base_url,
    "sheets": base_url + "/{}",
    "values": base_url + "/{}/values/{}",
}

sheets_config = GoogleSheetConfig()


def update_sheet_values(spreadsheetId: str, sheet_range: str, request_body: dict, majorDimension: str = "ROWS",
                        valueInputOption: str = "USER_ENTERED",
                        includeValuesInResponse: bool = False,
                        responseValueRenderOption: str = "FORMATTED_VALUE",
                        responseDateTimeRenderOption: str = "FORMATTED_STRING"):
    """
    :param spreadsheetId: The ID of the spreadsheet to update.
    :param sheet_range: The A1 notation of the values to update.
    :param request_body: Request Body.
    :param majorDimension: The major dimension of the values.
    :param valueInputOption: How the input data should be interpreted.
    :param includeValuesInResponse: True if grid data should be returned. This parameter is ignored if a field mask was set in the request.
    :param responseValueRenderOption: How values should be represented in the output.
    :param responseDateTimeRenderOption: How values should be rendered in the output.
    :return:
    """
    url = urls["values"].format(spreadsheetId, sheet_range)
    queryParm = {"valueInputOption": valueInputOption,
                 "includeValuesInResponse": includeValuesInResponse,
                 "responseValueRenderOption": responseValueRenderOption,
                 "responseDateTimeRenderOption": responseDateTimeRenderOption}
    res = put_call(url, json.dumps(request_body), queryParm)
    return res


def get_sheet_values(spreadsheetId: str, sheet_range: str, majorDimension: str = "ROWS",
                     valueRenderOption: str = "FORMATTED_VALUE",
                     dateTimeRenderOption: str = "FORMATTED_STRING"):
    """
    :param spreadsheetId: str, The ID of the spreadsheet to retrieve data from.
    :param sheet_range: str, The A1 notation or R1C1 notation of the range to retrieve values from.
    :param majorDimension: str, The major dimension that results should use.
    :param valueRenderOption: str, How values should be represented in the output.
    :param dateTimeRenderOption: str, how values should be rendered in the output.
    :return:
    """
    url = urls["values"].format(spreadsheetId, sheet_range)
    queryParm = {"majorDimension": majorDimension,
                 "valueRenderOption": valueRenderOption,
                 "dateTimeRenderOption": dateTimeRenderOption}
    res = get_call(url, queryParm)
    return res


def get_sheet(spreadsheetId: str, includeGridData: bool = False, *ranges: List[str]):
    """
    :param spreadsheetId: string, The spreadsheet to request. (required)
    :param includeGridData: boolean, True if grid data should be returned. This parameter is ignored if a field mask was set in the request.
    :param ranges: str, boolean, The ranges to retrieve from the spreadsheet. (repeated)
    :return:
    """
    url = urls["sheets"].format(spreadsheetId)
    queryParm = {"ranges": r for r in ranges}
    queryParm["includeGridData"] = includeGridData
    res = get_call(url, queryParm)
    return res


def put_call(url: str, request_body: str, queryParm: dict = None):
    queryParm = {} if queryParm is None else queryParm
    session = sheets_config.get_session()
    res = session.put(url, params=queryParm, data=request_body)
    if res.ok:
        return res.json()
    elif res.status_code == 429:
        logger.error('Too many requests. Sleeping %s' % res.text)
    else:
        logger.error('Failed to generate access token')
        logger.error("%d:%s" % (res.status_code, res.text))
    return res.json()


def get_call(url: str, queryParm: dict = ""):
    queryParm = {} if queryParm is None else queryParm
    session = sheets_config.get_session()
    res = session.get(url, params=queryParm)
    if res.ok:
        return res.json()
    elif res.status_code == 429:
        logger.error('Too many requests. Sleeping %s' % res.text)
    else:
        logger.error('Failed to generate access token')
        logger.error("%d:%s" % (res.status_code, res.text))
    return res.json()


if __name__ == '__main__':
    logger.info("Loading Sheet Utility.")
    response = get_sheet("1IsS3kkafb_sBo2FqTSmCq_cRau85JvchLZkxdVrA1G0")
    print(response)
    response = get_sheet_values("1IsS3kkafb_sBo2FqTSmCq_cRau85JvchLZkxdVrA1G0", "Scans!A1:B4")
    print(response)
