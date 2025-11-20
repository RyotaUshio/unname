import shutil
import subprocess
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


def get_excluded_paths(exclude_globs: list[str]) -> set[str]:
    excluded_paths = set(
        str(path)
        for exclude_glob in exclude_globs
        for path in Path('.').glob(exclude_glob)
    )
    return excluded_paths


def copy_tracked_files(outdir: Path, exclude_globs: list[str]):
    tracked_files = get_tracked_files()
    excluded_paths = get_excluded_paths(exclude_globs)

    for file in tracked_files:
        if file in excluded_paths:
            continue
        outfile = outdir / file
        outfile.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(file, outfile)
