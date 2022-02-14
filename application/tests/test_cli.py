import pytest

from typer.testing import CliRunner

from application import __application__, __version__
from {{name}} import cli


runner = CliRunner()


def test_cli_version():
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert f"{__application__}: {__version__}\n" in result.stdout
