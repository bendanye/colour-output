import json
import sys

from pathlib import Path

from args import Args
from rule import Rule
from typing import List
from rule_engine import get_matching_rule, apply_rule
from arg_parser import parse


def main(json_file_path: str) -> None:
    _validate_file_exists(json_file_path)

    args = _get_args(json_file_path)

    _validate_file_exists(args.color_file_path)

    print("specific_datetime: " + str(args.extra_args["specific_datetime"]))

    rules = _get_rules(json_file_path)

    with open(args.color_file_path, "r") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            _apply(rules, line, args)


def _validate_file_exists(file_path: str) -> None:
    my_file = Path(file_path)
    if not my_file.exists():
        raise ValueError(f"{file_path} does not exists")


def _get_args(json_file_path: str) -> Args:
    with open(json_file_path) as file:
        json_obj = json.load(file)
        return parse(json_obj["args"])


def _get_rules(json_file_path: str) -> List[Rule]:
    rules = []
    with open(json_file_path) as file:
        json_obj = json.load(file)
        for rule_obj in json_obj["rules"]:
            rules.append(Rule.from_dict(rule_obj))

    return rules


def _apply(rules: List[Rule], line: str, args: Args) -> None:
    rule = get_matching_rule(line, rules, args.extra_args)
    if rule:
        print(apply_rule(line, rule))
    else:
        print(line)


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Specify json file")
        exit(1)

    main(
        json_file_path=sys.argv[1],
    )
