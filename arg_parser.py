from args import Args
from datetime import datetime, timedelta


def parse(json_obj):
    if "extra_args" not in json_obj:
        return Args(color_file_path=json_obj["color_file_path"])

    extra_args = {}
    for obj in json_obj["extra_args"]:
        for key in obj:
            value = obj[key]
            extra_args[key] = _parse_time_expression(value)
    return Args(color_file_path=json_obj["color_file_path"], extra_args=extra_args)


def _now() -> datetime:
    return datetime.now()


def _parse_time_expression(expression: str):
    if expression.startswith("now()"):
        # Extract the time delta value (e.g., "5m" for 5 minutes)
        time_delta_part = expression.split("-")[1].strip()

        # Parse the time unit and value
        value = int(time_delta_part[:-1])
        unit = time_delta_part[-1]

        # Get the current time
        current_time = _now()

        # Calculate the new time based on the unit
        if unit == "m":
            return current_time - timedelta(minutes=value)
        elif unit == "h":
            return current_time - timedelta(hours=value)
        elif unit == "d":
            return current_time - timedelta(days=value)
        # Add more cases as needed

    return None
