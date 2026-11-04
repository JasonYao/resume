import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FLORILEGIUM = ROOT / "vendors" / "florilegium"


def test_florilegium_submodule_is_registered():
    result = subprocess.run(
        ["git", "config", "--file", ".gitmodules", "--get", "submodule.vendors/florilegium.path"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip() == "vendors/florilegium"


def test_florilegium_sparse_checkout_has_build_files():
    # bin/fetch_florilegium must have been run (CI does this before testing)
    assert (FLORILEGIUM / "florilegium.sty").is_file()
    lua_modules = {path.name for path in FLORILEGIUM.glob("florilegium*.lua")}
    assert {"florilegium.lua", "florilegium-grow.lua", "florilegium-ink.lua"} <= lua_modules


def test_florilegium_sparse_checkout_excludes_everything_else():
    unexpected = [
        path.name
        for path in FLORILEGIUM.iterdir()
        if path.name != ".git" and not path.name.startswith("florilegium")
    ]

    assert unexpected == []


def test_florilegium_exposes_the_region_api_used_by_the_layer():
    grow = (FLORILEGIUM / "florilegium-grow.lua").read_text()
    layer = (ROOT / "florilegium_layer.tex").read_text()

    assert 'require("florilegium-grow")' in layer
    assert "subtract_regions" in grow
