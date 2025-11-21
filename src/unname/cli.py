import argparse
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from .anonymize import anonymize_package
from .get_packages import PyprojectTomlNotFoundError, get_packages
from .logger import logger
from .prepare_outdir import prepare_outdir


def get_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return 'unknown'


def parse_args():
    parser = argparse.ArgumentParser(
        prog='unname',
        description='Anonymize Python codebases for blind review.',
    )
    parser.add_argument(
        '-o', '--output', type=Path, required=True, help='output directory'
    )
    parser.add_argument(
        '--exclude',
        type=str,
        nargs='*',
        default=['**/LICEN[CS]E', '**/LICEN[CS]E.*'],
        help='glob patterns to exclude from output (default: %(default)s)',
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version=f'{parser.prog} {get_version(parser.prog)}',
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    prepare_outdir(args.output, args.exclude)

    try:
        packages = get_packages(args.output)
    except PyprojectTomlNotFoundError as e:
        logger.error(e)
        return sys.exit(1)

    for package in packages:
        anonymize_package(package)


if __name__ == '__main__':
    main()
