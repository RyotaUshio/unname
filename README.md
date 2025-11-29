# unname

A simple CLI for anonymizing Python codebases for blind review.

It anonymizes `pyproject.toml` and `README.md` in your project (see below for details).
If your project is a [uv workspace](https://docs.astral.sh/uv/concepts/projects/workspaces), it anonymizes all workspace members.

## Prerequisite

Your project must be a git repository since `unname` internally uses `git ls-files` to filter out `.gitignore`d files.

## Usage

### Quickstart

Using [uv](https://docs.astral.sh/uv):

```sh
uvx unname -o <OUTPUT_DIRECTORY>
```

This will create an _anonymized copy_ of your project in `<OUTPUT_DIRECTORY>`.

You could also run `grep -r "Your Name" <OUTPUT_DIRECTORY>` to verify your name is not accidentally left in the git repository.

### Recommended setup

1. Create `scripts/anonymize` with the following content:
    ```sh
    #!/usr/bin/env bash
    
    uvx unname -o .unname/code --exclude scripts/anonymize
    zip .unname/code.zip -r .unname/code
    ```
2. Make it executable: `chmod +x scripts/anonymize`
3. Add `.unname` to your `.gitignore`
4. Run `./scripts/anonymize` to create an anonymized zip file at `.unname/code.zip`

## What it does

### 1. Make a copy of your project

First of all, `unname` will create a copy of your project in the directory specified by the `-o` or `--output` option.

`unname` only copies git-tracked files so that you don't have to manually filter out irrelevant files such as `.venv` from your code submission.

Furthermore, you can provide a list of file paths or glob patterns to exclude from output.
By default, `unname` excludes license files (`**/LICEN[CS]E`, `**/LICEN[CS]E.*`) and `**/.gitignore`.
To add more patterns to exclude, use the `-x` or `--exclude` option.
To override the default patterns, use the `-X` option.

### 2. pyproject.toml anonymization

`project.authors`, `project.maintainers` and `project.urls` fields will be removed (if they exist).

### 3. README.md anonymization

The content between `<!-- begin-unname -->` and `<!-- end-unname -->` will be removed.
For example:

#### Input

```md
# My Awesome Project

Code for the paper "My Awesome Method."

<!-- begin-unname -->
- Authors: Alice & Bob
- arXiv link: https://arxiv.org/abs/1234.56789
<!-- end-unname -->

## Install

...
```

#### Output

```md
# My Awesome Project

Code for the paper "My Awesome Method."

## Install

...
```
