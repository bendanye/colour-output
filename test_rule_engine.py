from datetime import datetime

from rule import Rule
from rule_engine import get_matching_rule, apply_rule


def test_get_matching_rule_should_get_when_match_with_contains():
    rule = Rule(criteria="contains Passed", colour_by="word", colour="NA")
    assert get_matching_rule("this is Passed by flying colour", [rule]) == rule


def test_get_matching_rule_should_not_get_when_not_match():
    rule = Rule(criteria="contains Failed", colour_by="word", colour="NA")
    assert get_matching_rule("this is Passed by flying colour", [rule]) is None


def test_get_matching_rule_should_get_when_timestamp_before_specific_datetime():
    specific_datetime = datetime.now()
    rule = Rule(
        criteria="timestamp[1] before ${specific_datetime}",
        colour_by="line",
        colour="NA",
    )
    assert (
        get_matching_rule(
            "scheduled at 2024-08-05 10:33:55.310000",
            [rule],
            extra_args={"specific_datetime": specific_datetime},
        )
        == rule
    )


def test_get_matching_rule_should_not_get_when_timestamp_after_specific_datetime():
    specific_datetime = datetime(2009, 8, 5, 18, 00)
    rule = Rule(
        criteria="timestamp[1] before ${specific_datetime}",
        colour_by="word",
        colour="NA",
    )
    assert (
        get_matching_rule(
            "scheduled at 2024-08-05 10:33:55.310000",
            [rule],
            extra_args={"specific_datetime": specific_datetime},
        )
        is None
    )


def test_apply_rule_should_get_colour_word():
    rule = Rule(criteria="contains Passed", colour_by="word", colour="green")
    assert (
        apply_rule("this is Passed by flying colour", rule)
        == "this is \x1b[32mPassed\x1b[0m by flying colour"
    )


def test_apply_rule_should_get_colour_line():
    rule = Rule(
        criteria="timestamp[1] before ${specific_datetime}",
        colour_by="line",
        colour="red",
    )
    assert (
        apply_rule("scheduled at 2024-08-05 10:33:55.310000", rule)
        == "\x1b[31mscheduled at 2024-08-05 10:33:55.310000\x1b[0m"
    )
