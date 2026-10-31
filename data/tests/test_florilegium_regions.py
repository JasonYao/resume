import os
import shutil
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
FLORILEGIUM_TEST = ROOT / "venders" / "florilegium" / "tests" / "regions.tex"


def test_florilegium_region_harness(tmp_path):
    texlive_bin = Path("/tmp/texlive/bin/x86_64-linux")
    lualatex = shutil.which("lualatex") or str(texlive_bin / "lualatex")
    if not Path(lualatex).is_file():
        pytest.skip("LuaLaTeX is not installed")

    env = os.environ.copy()
    env["PATH"] = f"{texlive_bin}:{env.get('PATH', '')}"
    env["TEXINPUTS"] = f"{ROOT / 'venders' / 'florilegium'}//:{env.get('TEXINPUTS', '')}"
    env["LUAINPUTS"] = f"{ROOT / 'venders' / 'florilegium'}//:{env.get('LUAINPUTS', '')}"
    result = subprocess.run(
        [
            lualatex,
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={tmp_path}",
            FLORILEGIUM_TEST.name,
        ],
        cwd=FLORILEGIUM_TEST.parent,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert (tmp_path / "regions.pdf").is_file()
    assert "Output written on regions.pdf (3 pages," in result.stdout
