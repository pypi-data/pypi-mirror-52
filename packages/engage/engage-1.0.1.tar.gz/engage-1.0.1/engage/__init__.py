from pathlib import Path

from engage.traverse import traverse, get_contents
from engage.writer import update_module, Sphinx, Writer


def engage_path(file_path: str, writer: Writer=Sphinx):
    for file in traverse(Path(file_path)):
        new_file = update_module(
            get_contents(str(file)),
            writer
        )
        with open(file, "w") as f:
            f.write(new_file)
