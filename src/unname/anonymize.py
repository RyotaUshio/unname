from pathlib import Path

import tomlkit
import tomlkit.api  # necessary to make type checkers happy

from .logger import logger


def anonymize_package(path: Path) -> None:
    anonymize_pyproject_toml(path / 'pyproject.toml')
    anonymize_readme_md(path / 'README.md')


def anonymize_pyproject_toml(path: Path) -> None:
    try:
        with open(path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        logger.warning(f'pyproject.toml not found at {path}, skipping')
        return

    anonymized_content = anonymize_pyproject_toml_content(content)

    with open(path, 'w') as f:
        f.write(anonymized_content)


def anonymize_pyproject_toml_content(content: str) -> str:
    doc = tomlkit.parse(content)

    project = doc['project']
    if not isinstance(project, tomlkit.api.Table):
        raise ValueError('invalid pyproject.toml: project is not a table')

    if 'authors' in project:
        project.remove('authors')
    if 'maintainers' in project:
        project.remove('maintainers')
    if 'urls' in project:
        project.remove('urls')

    anonymized_content = tomlkit.dumps(doc)
    return anonymized_content


class ReadmeParseError(Exception):
    pass


def anonymize_readme_md(path: Path) -> None:
    try:
        with open(path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        logger.warning(f'README.md not found at {path}, skipping')
        return

    anonymized_content = anonymize_readme_md_content(content)

    with open(path, 'w') as f:
        f.write(anonymized_content)


def anonymize_readme_md_content(content: str) -> str:
    def is_begin(line: str) -> bool:
        return line.strip().lower() == '<!-- begin-unname -->'

    def is_end(line: str) -> bool:
        return line.strip().lower() == '<!-- end-unname -->'

    lines = content.splitlines(keepends=True)
    anonymized_lines: list[str] = []
    count = 0
    for line in lines:
        if is_begin(line):
            count += 1

        match count:
            case 0:
                anonymized_lines.append(line)
            case 1:
                pass
            case _:
                raise ReadmeParseError(
                    'Unmatched begin-unname/end-unname markers'
                )

        if is_end(line):
            count -= 1

    anonymized_content = ''.join(anonymized_lines)
    return anonymized_content
