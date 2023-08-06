from datetime import datetime, timedelta, timezone

import pytest

from bluejay.backend.encode import JSONEncoder, datetime_to_rfc3339

# fmt: off
# Black will change the last datetime to have arguments on separate lines.
date_time_to_expected = [
    (datetime(2018, 9, 12, 10, 56, 43, 343), '2018-09-12T10:56:43.000343'),
    (datetime(2018, 12, 30, 23, 23, 0, 0), '2018-12-30T23:23:00'),
    (
        datetime(2018, 12, 30, 23, 23, 0, 0, tzinfo=timezone(timedelta(hours=2))),
        '2018-12-30T23:23:00+02:00'
    ),
    (
        datetime(2018, 12, 30, 23, 23, 0, 0, tzinfo=timezone(-timedelta(hours=3, minutes=43))),
        '2018-12-30T23:23:00-03:43'
    ),
    (
        datetime(2018, 12, 30, 23, 23, 32, 7065, tzinfo=timezone(timedelta(hours=5, minutes=30))),
        '2018-12-30T23:23:32.007065+05:30'
    ),
]
# fmt: on


@pytest.mark.parametrize(["dt", "expected"], date_time_to_expected)
def test_datetime_is_converted_to_rfc3339_format(dt, expected):
    formatted = datetime_to_rfc3339(dt)
    assert expected == formatted


@pytest.mark.parametrize(["dt", "expected"], date_time_to_expected)
def test_json_encoder_encodes_datetimes(faker, dt, expected):
    key = faker.pystr()
    input = {key: dt}
    output = JSONEncoder().encode(input)
    expected_output = '{{"{key}": "{expected}"}}'.format(key=key, expected=expected)
    assert expected_output == output
