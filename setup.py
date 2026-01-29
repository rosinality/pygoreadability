from __future__ import annotations

import os
import subprocess
from pathlib import Path

from setuptools import setup
from setuptools.dist import Distribution
from setuptools.command.build_py import build_py
from wheel.bdist_wheel import bdist_wheel


ROOT = Path(__file__).resolve().parent


def _parse_pyproject_metadata() -> tuple[str | None, str | None]:
    pyproject = ROOT / "pyproject.toml"
    if not pyproject.is_file():
        return None, None
    name = None
    version = None
    in_project = False
    with pyproject.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                in_project = line == "[project]"
                continue
            if not in_project or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            if key == "name":
                name = value
            elif key == "version":
                version = value
            if name and version:
                break
    return name, version


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


setup(
    name=_parse_pyproject_metadata()[0],
    version=_parse_pyproject_metadata()[1],
    cmdclass={"build_py": BuildPy, "bdist_wheel": BDistWheel},
    distclass=BinaryDistribution,
)
