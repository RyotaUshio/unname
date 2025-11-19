from pathlib import Path

import tomlkit


def anonymize_package(path: Path) -> None:
    anonymize_pyproject_toml(path / 'pyproject.toml')
    anonymize_readme_md(path / 'README.md')


def anonymize_pyproject_toml(path: Path) -> None:
    with open(path, 'r') as f:
        pyproject = tomlkit.load(f)

    authors = pyproject['project'].get('authors')
    if authors:
        pyproject['project']['authors'] = []
    maintainers = pyproject['project'].get('maintainers')
    if maintainers:
        pyproject['project']['maintainers'] = []

    with open(path, 'w') as f:
        tomlkit.dump(pyproject, f)


class ReadmeParseError(Exception):
    pass


def anonymize_readme_md(path: Path) -> None:
    def is_begin(line: str) -> bool:
        return line.strip().lower() == '<!-- begin-unname -->'

    def is_end(line: str) -> bool:
        return line.strip().lower() == '<!-- end-unname -->'

    with open(path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    count = 0
    for line in lines:
        if is_begin(line):
            count += 1

        match count:
            case 0:
                new_lines.append(line)
            case 1:
                pass
            case _:
                raise ReadmeParseError(
                    'Unmatched begin-unname/end-unname markers'
                )

        if is_end(line):
            count -= 1

    with open(path, 'w') as f:
        f.writelines(new_lines)
