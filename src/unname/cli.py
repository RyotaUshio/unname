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
            '--exclude',
            type=str,
            nargs='*',
            default=['**/LICEN[CS]E', '**/LICEN[CS]E.*', '**/.gitignore'],
            help='glob patterns to exclude from output (default: %(default)s)',
        )
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=f'{parser.prog} {get_version(parser.prog)}',
        )
        args = parser.parse_args()

        options = Options.model_validate(args, from_attributes=True)
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
