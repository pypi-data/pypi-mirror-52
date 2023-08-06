from pathlib import Path
from typing import List
from os import listdir


def traverse(path: Path) -> List[Path]:
    if path.is_file():
        return [path]
    else:
        parts = listdir(str(path))
        if '__init__.py' in parts:
            return sum([traverse(path.joinpath(part)) for part in parts], [])
        return []


def get_contents(file_path: str):
    with open(file_path) as f:
        return f.read()
