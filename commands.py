#!/usr/bin/env python3
# coding: utf-8

"""Typer cli interface to quickly manage the project"""

import subprocess
from pathlib import Path

import typer

from rich import inspect
from rich.markdown import Markdown

from application.console import console
from application.config import settings as app_settings


#----------CONFIG--------------------------------------------------------------
cli = typer.Typer()
CWD = Path(__file__).parent.absolute()

# ---------HELPERS-------------------------------------------------------------
def echo(
    message: str,
    fg_color: str = typer.colors.WHITE,
    bg_color: str = typer.colors.BLACK,
    bold: bool = False
    ):
    """colors:
        "bright_" + black, red, green, yellow, blue, magenta, cyan, white
    """
    typer.echo(
        typer.style(
            message,
            fg=fg_color,
            bg=bg_color,
            bold=bold,
        )
    )

def delete_folder(path: Path):
    for element in path.iterdir():
        if element.is_dir():
            delete_folder(element)
        else:
            element.unlink()
    path.rmdir()

def clean_build():
    echo(f"Unlinking build-files: build/; dist/ *.egg-info; __pycache__;", fg_color=typer.colors.RED)
    cwd = Path(CWD)
    [delete_folder(p) for p in cwd.rglob('build')]
    [delete_folder(p) for p in cwd.rglob('*.egg-info')]
    [delete_folder(p) for p in cwd.rglob('__pycache__')]
    [delete_folder(p) for p in cwd.rglob('.pytest_cache')]
    try:
        [delete_folder(p) for p in cwd.rglob('dist')]
    except OSError as err:
        echo(f"Error deleting dist-folder: {err}", fg_color=typer.colors.RED)

def clean_pyc():
    echo(f"Unlinking caches: *.pyc; *pyo; *~;", fg_color=typer.colors.RED)
    [p.unlink() for p in Path(CWD).rglob('*.py[co]')]
    [p.unlink() for p in Path(CWD).rglob('*~')]

def run_command(command, debug=False, cwd=CWD, env=None, shell=False):
    if debug:
        echo(f">>> Running command: {command}")
    try:
        subprocess.run(command.split(), cwd=cwd, env=env, shell=shell)
    except FileNotFoundError:
        echo(f'The command {command} threw a FileNotFoundError', fg_color=typer.colors.RED)


#----------GENERAL COMMANDS----------------------------------------------------
@cli.command()
def clean():
    """Cleaning pycache, buildfiles"""
    clean_build()
    clean_pyc()

@cli.command()
def black(path: str = typer.Argument(None)):
    """black <path>"""
    command = "black"
    if path is not None:
        command = f"{command} {path}"
    run_command(command)

@cli.command()
def pytest(test_path: str = typer.Argument(None)):
    """pytest <path>"""
    command = "pytest"
    if test_path is not None:
        command = f"{command} {test_path}"
    run_command(command)

@cli.command()
def test(test_path: str = typer.Argument(None), skip: bool = False):
    """test"""
    pytest(test_path)

@cli.command()
def rebuild():
    """= clean + initialize"""
    clean()
    initialize()

@cli.command()
def initialize():
    """Initialize & setup of the projects environment ..."""
    echo(f'Successfully finsihed: {initialize.__doc__} ', fg_color=typer.colors.GREEN)


# ---------- ABBREVIATIONS ----------------------------------------------------
@cli.command()
def rb():
    "= rebuild"
    rebuild()

@cli.command()
def init():
    "= initialize"
    initialize()

@cli.command()
def up():
    """= run (start the script)"""
    run()


# ---------- INTROSPECTION ----------------------------------------------------
@cli.command()
def readme():
    """README"""
    with open("README.md") as readme:
        markdown = Markdown(readme.read())
    console.print(markdown)

@cli.command()
def settings():
    """debugging output"""
    inspect(app_settings)


# ---------- MANAGE THE SERVER -------------------------------------------------
@cli.command()
def run(
):  # pragma: no cover
    """
    Run the script.
    """
    ...


if __name__ == "__main__":
    cli()
