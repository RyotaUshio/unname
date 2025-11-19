from glob import glob
from pathlib import Path
from typing import cast

import tomlkit


def get_packages() -> list[Path]:
    with open('pyproject.toml', 'r') as f:
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
            Path(package)
            for package_glob in package_globs
            for package in glob(package_glob)
        ]
        assert all(package.exists() for package in packages)
        return packages
