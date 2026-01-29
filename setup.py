from __future__ import annotations

import os
import subprocess
from pathlib import Path

from setuptools import setup
from setuptools.dist import Distribution
from setuptools.command.build_py import build_py
from wheel.bdist_wheel import bdist_wheel


ROOT = Path(__file__).resolve().parent


def _parse_pyproject_metadata() -> tuple[str, str]:
    pyproject = ROOT / "pyproject.toml"
    if not pyproject.is_file():
        raise RuntimeError("pyproject.toml not found; cannot read package metadata")
    try:
        import tomllib
    except ModuleNotFoundError:  # Python < 3.11
        import tomli as tomllib
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    project = data.get("project", {})
    name = project.get("name")
    version = project.get("version")
    if not name or not version:
        raise RuntimeError("Missing name/version in pyproject.toml [project]")
    return str(name), str(version)


class BuildPy(build_py):
    def run(self) -> None:
        # Ensure the shared library is built before packaging.
        if os.environ.get("PYGOREADABILITY_SKIP_BUILD") != "1":
            subprocess.check_call(["bash", "scripts/build_lib.sh"], cwd=ROOT)
        super().run()


class BDistWheel(bdist_wheel):
    def finalize_options(self) -> None:
        super().finalize_options()
        # Ensure the wheel is tagged as platform-specific because it bundles a shared library.
        self.root_is_pure = False


class BinaryDistribution(Distribution):
    def has_ext_modules(self) -> bool:
        return True


_name, _version = _parse_pyproject_metadata()

setup(
    name=_name,
    version=_version,
    cmdclass={"build_py": BuildPy, "bdist_wheel": BDistWheel},
    distclass=BinaryDistribution,
)
