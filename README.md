# unname

A simple CLI for anonymizing Python codebases for blind review.

It anonymizes `pyproject.toml` and `README.md` in your project (see below for details).
If your project is a [uv workspace](https://docs.astral.sh/uv/concepts/projects/workspaces), it anonymizes all workspace members.

## Usage

Using [uv](https://docs.astral.sh/uv):

```sh
# Files will be overwritten in-place, so make sure you commit your edits and
# make a new branch before running
git switch -c anon
uvx unname
```

You can also run `git grep "Your Name"` to verify your name is not accidentaly left in the git repository.

## What it does

### pyproject.toml anonymization

`authors` and `maintainers` fields will be replaced with an empty list (if they exist).

### README.md anonymization

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
