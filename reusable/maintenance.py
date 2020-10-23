import json
import os
import time
from datetime import datetime

# time parser ISO8601
import re
from pprint import pprint
from operator import mul
from itertools import accumulate
from typing import Pattern, List


def file_write_json(data, filename, ext=None):
    #   TODO: changes 10/9/20 ensure compatibility with YouTube impl
    if ext:
        filename = filename + "_" + set_timestamp() + "." + ext
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return filename


def file_read_json(filename):
    # while not os.path.exists(filename):
    #     pass  # time.sleep(1)
    if os.path.isfile(filename):
        with open(filename) as f:
            return json.load(f)
    else:
        raise ValueError("%s isn't a file!" % filename)


def get_timestamp(time_format='%m,%d,%y,%H:%M:%S'):
    t = time.localtime()
    return time.strftime(time_format, t)


def set_timestamp():
    t = time.localtime()
    return time.strftime('%m%d%y%H%M%S', t)


def get_date_iso(str_date):
    return datetime.fromisoformat(str_date.replace("Z", "+00:00")).date()


def parse_udration(str_pattern):
    # see http://en.wikipedia.org/wiki/ISO_8601#Durations
    ISO_8601_period_rx = re.compile(
        'P'  # designates a period
        '(?:(?P<years>\d+)Y)?'  # years
        '(?:(?P<months>\d+)M)?'  # months
        '(?:(?P<weeks>\d+)W)?'  # weeks
        '(?:(?P<days>\d+)D)?'  # days
        '(?:T'  # time part must begin with a T
        '(?:(?P<hours>\d+)H)?'  # hourss
        '(?:(?P<minutes>\d+)M)?'  # minutes
        '(?:(?P<seconds>\d+)S)?'  # seconds
        ')?'  # end of time part
    )

    # pprint(ISO_8601_period_rx.match('P1W2DT6H21M32S').groupdict())
    return ISO_8601_period_rx.match(str_pattern).groupdict()

    # {'days': '2',
    #  'hours': '6',
    #  'minutes': '21',
    #  'months': None,
    #  'seconds': '32',
    #  'weeks': '1',
    #  'years': None}


SECONDS_PER_SECOND = 1
SECONDS_PER_MINUTE: int = 60
MINUTES_PER_HOUR: int = 60
HOURS_PER_DAY: int = 24
DAYS_PER_WEEK: int = 7
WEEKS_PER_YEAR: int = 52

ISO8601_PATTERN = re.compile(
    r"P(?:(\d+)Y)?(?:(\d+)W)?(?:(\d+)D)?"
    r"T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?"
)


def extract_total_seconds_from_ISO8601(iso8601_duration: str) -> int:
    """Compute duration in seconds from a Youtube ISO8601 duration format. """
    MULTIPLIERS: List[int] = (
        SECONDS_PER_SECOND, SECONDS_PER_MINUTE, MINUTES_PER_HOUR,
        HOURS_PER_DAY, DAYS_PER_WEEK, WEEKS_PER_YEAR
    )
    groups: List[int] = [int(g) if g is not None else 0 for g in
                         ISO8601_PATTERN.match(iso8601_duration).groups()]

    return sum(g * multiplier for g, multiplier in
               zip(reversed(groups), accumulate(MULTIPLIERS, mul)))
