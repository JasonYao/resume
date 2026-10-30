import os
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "bin" / "distrust_emudhra"

pytestmark = pytest.mark.skipif(
  shutil.which("openssl") is None, reason="openssl is required"
)


def _make_cert(directory: Path, common_name: str) -> str:
  key, cert = directory / "k.pem", directory / "c.pem"
  subprocess.run(
    ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1",
     "-subj", f"/CN={common_name}", "-keyout", str(key), "-out", str(cert)],
    check=True, capture_output=True,
  )
  return cert.read_text()


def test_filter_removes_only_emudhra_certs(tmp_path):
  emudhra = _make_cert(tmp_path, "emSign Root CA - G1")
  other = _make_cert(tmp_path, "Some Other Root CA")
  bundle = tmp_path / "bundle.pem"
  bundle.write_text(emudhra + other)

  subprocess.run([str(SCRIPT), "filter", str(bundle)], check=True, capture_output=True)

  assert bundle.read_text().strip() == other.strip()


@pytest.mark.skipif(not os.environ.get("CI"), reason="only enforced in CI")
def test_ci_trust_stores_do_not_trust_emudhra():
  result = subprocess.run([str(SCRIPT), "verify"], capture_output=True, text=True)
  assert result.returncode == 0, result.stdout + result.stderr
