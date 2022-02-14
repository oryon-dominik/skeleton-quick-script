import toml
from .paths import ROOT_DIR

project = toml.load(ROOT_DIR / "pyproject.toml")

name = project["tool"]["poetry"]['name']
version = project["tool"]["poetry"]['version']
