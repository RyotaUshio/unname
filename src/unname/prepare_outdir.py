import shutil
import subprocess
from pathlib import Path


def prepare_outdir(outdir: Path):
    cleanup_outdir(outdir)
    copy_tracked_files(outdir)


def cleanup_outdir(outdir: Path):
    if outdir.exists():
        shutil.rmtree(outdir)


def copy_tracked_files(outdir: Path):
    tracked_files = subprocess.run(
        ['git', 'ls-files'],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()

    for file in tracked_files:
        assert Path(file).is_file()
        outfile = outdir / file
        outfile.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(file, outfile)
