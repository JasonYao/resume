from pathlib import Path
import re

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
APT_SETUP_FILES = (
  REPOSITORY_ROOT / ".github" / "workflows" / "copilot-setup-steps.yml",
  REPOSITORY_ROOT / ".github" / "workflows" / "main.yml",
  REPOSITORY_ROOT / "bin" / "install_dependencies",
)


def test_apt_setup_uses_stable_cli():
  for path in APT_SETUP_FILES:
    assert re.search(r"\bsudo apt(?:\s|$)", path.read_text()) is None


def test_imagemagick_install_includes_alternatives_manpages():
  install_script = (REPOSITORY_ROOT / "bin" / "install_dependencies").read_text()

  assert "Dpkg::Options::=--path-include=/usr/share/man/*" in install_script
