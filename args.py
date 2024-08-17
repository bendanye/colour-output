from dataclasses import dataclass
from typing import Optional


@dataclass
class Args:
    color_file_path: str
    extra_args: Optional[dict] = None
