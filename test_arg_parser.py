from datetime import datetime, timedelta
from pytest_mock import MockFixture

from args import Args
from arg_parser import parse


def test_parse_file_path_should_success():
    json_obj = {"color_file_path": "/path/file.txt"}
    assert parse(json_obj) == Args(color_file_path="/path/file.txt")


def test_parse_extra_arg_with_specified_date_should_success(mocker: MockFixture):
    json_obj = {
        "color_file_path": "/path/file.txt",
        "extra_args": [{"specified_date": "now() - 5m"}],
    }
    mocked_datetime = mocker.patch(
        "arg_parser._now",
    )
    jan_31 = datetime(2023, 1, 31, 0, 5, 0)
    mocked_datetime.return_value = jan_31

    expected_specific_date = jan_31 - timedelta(minutes=5)
    assert parse(json_obj) == Args(
        color_file_path="/path/file.txt",
        extra_args={"specified_date": expected_specific_date},
    )
