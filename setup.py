from __future__ import annotations

import os
import subprocess
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py


ROOT = Path(__file__).resolve().parent


class BuildPy(build_py):
    def run(self) -> None:
        # Ensure the shared library is built before packaging.
        if os.environ.get("PYGOREADABILITY_SKIP_BUILD") != "1":
            subprocess.check_call(["bash", "scripts/build_lib.sh"], cwd=ROOT)
        super().run()


setup(
    cmdclass={"build_py": BuildPy},
)
