from __future__ import annotations

import argparse
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from pydantic import BaseModel

from .anonymize import anonymize_package
from .get_packages import PyprojectTomlNotFoundError, get_packages
from .logger import logger
from .prepare_outdir import prepare_outdir


def get_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return 'unknown'


DEFAULT_EXCLUDE = ['**/LICEN[CS]E', '**/LICEN[CS]E.*', '**/.gitignore']


class Options(BaseModel):
    output: Path
    exclude: list[str]

    @staticmethod
    def from_commandline() -> Options:
        parser = argparse.ArgumentParser(
            prog='unname',
            description='Anonymize Python codebases for blind review.',
        )
        parser.add_argument(
            '-o', '--output', type=Path, required=True, help='output directory'
        )
        parser.add_argument(
            '-x',
            '--exclude',
            type=str,
            nargs='*',
            default=[],
            help=(
                'Additional glob patterns to exclude from output. '
                'By default, %(prog)s excludes the following patterns: '
                + ', '.join(DEFAULT_EXCLUDE)
                + '. '
                'Use this option to add more patterns. '
                'To override the default patterns, use the -X option instead.'
            ),
        )
        parser.add_argument(
            '-X',
            type=str,
            nargs='*',
            help='glob patterns to exclude from output, overriding the default patterns',
        )
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=f'{parser.prog} {get_version(parser.prog)}',
        )
        args = parser.parse_args()

        options = Options(
            output=args.output,
            exclude=args.X or (DEFAULT_EXCLUDE + args.exclude),
        )
        return options


def main():
    options = Options.from_commandline()
    prepare_outdir(options.output, options.exclude)

    try:
        packages = get_packages(options.output)
    except PyprojectTomlNotFoundError as e:
        logger.error(e)
        return sys.exit(1)

    for package in packages:
        anonymize_package(package)


if __name__ == '__main__':
    main()
