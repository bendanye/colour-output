import re

from typing import List

from rule import Rule
from datetime import datetime

RED_COLOR = "31"
GREEN_COLOR = "32"
YELLOW_COLOR = "33"
BLUE_COLOR = "34"

COLOR_MAPPING = {
    "red": RED_COLOR,
    "green": GREEN_COLOR,
    "yellow": YELLOW_COLOR,
    "blue": BLUE_COLOR,
}


def get_matching_rule(line: str, rules: List[Rule], extra_args=None):
    if extra_args is None:
        extra_args = {}

    for rule in rules:
        if " and " in rule.criteria:
            founds = []
            criterias = rule.criteria.split(" and ")
            for criteria in criterias:
                found = _check_rule(line, rule, criteria, extra_args)
                if found:
                    founds.append(found)

            if len(founds) == len(criterias):
                return founds[0]
        else:
            found = _check_rule(line, rule, rule.criteria, extra_args)
            if found:
                return found

    return None


def _check_rule(line: str, rule: Rule, criteria: str, extra_args) -> bool:
    if "contains " in criteria:
        criteria = criteria.replace("contains ", "")
        if re.search(criteria, line):
            return rule

    if "timestamp" in criteria:
        timestamp_match = re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", line)
        if not timestamp_match:
            raise ValueError("Timestamp not found in the input string")

        timestamp_str = timestamp_match.group(0)
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")

        # Parse the rule to extract the date key
        rule_match = re.search(r"\$\{(\w+)\}", criteria)
        if not rule_match:
            raise ValueError("Rule does not contain a valid date key")

        date_key = rule_match.group(1)

        # Retrieve the specified date from the dictionary
        specified_date = extra_args.get(date_key)
        if not specified_date:
            raise ValueError(f"Date key '{date_key}' not found in the date dictionary")

        if not isinstance(specified_date, datetime):
            raise ValueError(
                f"The value for the key '{date_key}' is not a datetime object"
            )

        pattern = r"timestamp.*\s+(\w+)\s+\.*"
        match = re.search(pattern, criteria)
        if not match:
            raise ValueError(f"timestamp compare operator not found")

        operator = match.group(1)
        if operator == "before" and timestamp < specified_date:
            return rule
        if operator == "after" and timestamp > specified_date:
            return rule


def apply_rule(line: str, rule: Rule) -> str:
    if rule.colour_by == "word":
        if "contains " in rule.criteria:
            word = rule.criteria.replace("contains ", "")
            colored_sentence = line.replace(
                word, _color_text(word, COLOR_MAPPING[rule.colour])
            )
            return colored_sentence
    elif rule.colour_by == "line":
        colored_sentence = _color_text(line, COLOR_MAPPING[rule.colour])
        return colored_sentence


def _color_text(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"
