import logging
from datetime import datetime, timezone

logging.basicConfig(level=logging.DEBUG)

required_timezone = timezone.utc
CCYYMMDD_HHMMSS = "%Y%m%dT%H%M%S"
CCYY_MM_DD_HH_MM_SS = "%Y-%m-%dT%H:%M:%S.%fZ"

'''
https://docs.python.org/3/library/time.html
'''


def getTimeStamp(inputTimestamp: str, input_format: str = CCYY_MM_DD_HH_MM_SS):
    return get_date(inputTimestamp, input_format)


def get_date_from_unix(unix_time) -> datetime:
    input_datetime = datetime.utcfromtimestamp(unix_time)
    return input_datetime.replace(tzinfo=required_timezone)


def get_date(time_in_str: str, input_format: str) -> datetime:
    return datetime.strptime(time_in_str, input_format)


def getCurrentTimeStamp(fmt: str = None):
    if fmt:
        return datetime.now().strftime(fmt)
    else:
        return datetime.now().isoformat()


if __name__ == '__main__':
    logging.info("Loading Datetime utility.")
    time_stamp = getTimeStamp("2022-02-01T08:31:52.566Z")
    print(time_stamp)
    print(getCurrentTimeStamp())
    print(getCurrentTimeStamp("%Y-%m-%dT%H:%M:%S.%fZ"))
