from argparse import ArgumentParser

from engage import engage_path


parser = ArgumentParser()
parser.add_argument("package", help="The file / directory to engage")


if __name__ == "__main__":
    args = parser.parse_args()
    engage_path(args.package)
