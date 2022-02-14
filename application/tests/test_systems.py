import toml

from ..config.paths import ROOT_DIR


def test_version_loads_as_expected(version):
    project = toml.load(ROOT_DIR / "pyproject.toml")
    assert version == project["tool"]["poetry"]['version']
