from argparse import ArgumentParser

from mobikit_utils import __version__


def create_parser():
    parser = ArgumentParser("mobikit utilities")
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="show the mobikit utilities version",
    )
    return parser


def version():
    print(__version__)


def main():
    parser = create_parser()
    args = parser.parse_args()
    if args.version:
        version()
