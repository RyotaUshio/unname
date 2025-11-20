import glob
from pathlib import Path
from typing import cast

import tomlkit


def get_packages(outdir: Path) -> list[Path]:
    with open(outdir / 'pyproject.toml', 'r') as f:
        pyproject = tomlkit.load(f)

    package_globs = (
        cast(
            list[str] | None,
            pyproject.get('tool', {})
            .get('uv', {})
            .get('workspace', {})
            .get('members'),
        )
        or []
    )
    package_globs.insert(0, '.')
    packages = [
        outdir / package
        for package_glob in package_globs
        for package in glob.iglob(package_glob, root_dir=outdir)
    ]
    assert all(package.exists() for package in packages)
    return packages
