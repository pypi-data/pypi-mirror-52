import datetime
import enum
import json
import os
import pytz
import sys
import time


MIN_DATE = datetime.datetime(year=2000, month=1, day=1)
MAX_DATE = MIN_DATE + datetime.timedelta(days=100*365)
MIN_TS = MIN_DATE.timestamp()
MAX_TS = MAX_DATE.timestamp()
VERSION = '0.0.4'


def print_as_json(value):
  print(json.dumps(value, indent=2, default=str))


class UnitPerSec(enum.IntEnum):
    SEC = 1
    MILLI_SEC = int(1e3)
    MICRO_SEC = int(1e6)
    NANO_SEC = int(1e9)


class UnitName(enum.Enum):
    SEC = 'second'
    MILLI_SEC = 'millisecond'
    MICRO_SEC = 'microsecond'
    NANO_SEC = 'nanosecond'


def is_reasonable(ts: float):
    return MIN_TS <= ts <= MAX_TS


def check_interval():
    MAX_TS  < MIN_TS * UnitPerSec.MILLI_SEC


class InvalidTsValue(ValueError):
    pass


def guess_ts_unit(ts):
    ts = float(ts)
    for unit_per_sec in UnitPerSec:
        if is_reasonable(ts/unit_per_sec.value):
            return unit_per_sec
    raise InvalidTsValue('Timestamp value not in reasonable range!')


def ts_to_datetime(input_ts, tz):
    unit_per_sec = guess_ts_unit(input_ts)
    ts = float(input_ts) / unit_per_sec.value
    dt = datetime.datetime.fromtimestamp(ts, tz)
    return {
        'datetime': dt,
        'seconds': ts,
        'nanoseconds': int(ts * 1e9),
        'tz': tz,
        'input': input_ts,
        'unit': getattr(UnitName, unit_per_sec.name).value,
    }


def print_usage():
    program_name = sys.argv[0]
    print(f'{program_name} {VERSION}')
    print('usage:')
    print(f'\t{program_name} timestamp')


def main(argv=None):
    argv = argv or sys.argv
    check_interval()
    tz_str = os.environ.get('TZ', 'UTC')
    tzinfo = pytz.timezone(tz_str)

    try:
        timestamp = argv[1]  # str
        result = ts_to_datetime(timestamp, tzinfo)
        print_as_json(result)
    except InvalidTsValue:
        print(f'Reasonable time range [{MIN_DATE}, {MAX_DATE}]')
    except (IndexError, KeyError):
        print_usage()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
