import re
import json


def parse_str(s: str):
    return json.loads(s)


def parse_datetime(datetime):
    return [int(x) for x in filter(lambda s: len(s) <= 4, re.split('[-:/ .]', str(datetime)))]

