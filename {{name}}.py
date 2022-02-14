#!/usr/bin/env python3
# coding: utf-8

from typing import Optional

import typer

from application import __application__, __version__
from application.config import settings
from application.config.logs import logging
from application.console import console


log = logging.getLogger('application')
cli = typer.Typer()


def _version_callback(value: bool) -> None:
    """Print version."""
    if value:
        console.print(f"{__application__}: {__version__}")
        raise typer.Exit()


@cli.command()
def foo() -> None:
    """foo"""
    log.info("foo command")
    console.print(f"dotenv configured: {settings.ENV.exists()}")


@cli.callback()
def main(version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,  # processed upfront!
    )) -> None:
    f"""Cli interface for {__application__}."""
    console.rule(f"[bold blue]{__application__}")
    return  # NOSONAR


def main():
    cli(prog_name=__application__)

if __name__ == "__main__":
    main()
