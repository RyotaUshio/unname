from pathlib import Path

import tomlkit


def anonymize_package(path: Path) -> None:
    anonymize_pyproject_toml(path / "pyproject.toml")
    anonymize_readme(path / "README.md")


def anonymize_pyproject_toml(path: Path) -> None:
    with open(path, "r") as f:
        pyproject = tomlkit.load(f)

    authors = pyproject["project"].get("authors")
    if authors:
        pyproject["project"]["authors"] = []
    maintainers = pyproject["project"].get("maintainers")
    if maintainers:
        pyproject["project"]["maintainers"] = []

    with open(path, "w") as f:
        tomlkit.dump(pyproject, f)


def anonymize_readme(path: Path) -> None:
    def is_begin(line: str) -> bool:
        return line.strip().lower() == "<!-- begin-unname -->"

    def is_end(line: str) -> bool:
        return line.strip().lower() == "<!-- end-unname -->"

    with open(path, "r") as f:
        lines = f.readlines()

    with open(path, "w") as f:
        is_in_anon = False
        for line in lines:
            if is_begin(line):
                is_in_anon = True
            if is_end(line):
                is_in_anon = False

            if is_in_anon:
                continue
            f.write(line)
