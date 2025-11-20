import glob
import re
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path


def prepare_outdir(outdir: Path, exclude_globs: list[str]):
    cleanup_outdir(outdir)
    copy_tracked_files(outdir, exclude_globs)


def cleanup_outdir(outdir: Path):
    if outdir.exists():
        shutil.rmtree(outdir)


def get_tracked_files() -> list[str]:
    tracked_files = subprocess.run(
        ['git', 'ls-files'],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    return tracked_files


def create_exclude_checker(exclude_globs: list[str]) -> Callable[[str], bool]:
    patterns = [
        re.compile(glob.translate(exclude_glob))
        for exclude_glob in exclude_globs
    ]

    def is_excluded(file: str) -> bool:
        return any(pattern.match(file) for pattern in patterns)

    return is_excluded


def copy_tracked_files(outdir: Path, exclude_globs: list[str]):
    tracked_files = get_tracked_files()
    is_excluded = create_exclude_checker(exclude_globs)

    for file in tracked_files:
        if is_excluded(file):
            continue
        assert Path(file).is_file()
        outfile = outdir / file
        outfile.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(file, outfile)
