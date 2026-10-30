from os import environ as os_environ
from pathlib import Path
from shutil import which as shutil_which
from subprocess import run as subprocess_run

from pytest import mark as pytest_mark

SCRIPT = Path(__file__).resolve().parents[2] / "bin" / "lockdown"

pytestmark = pytest_mark.skipif(shutil_which("openssl") is None, reason="openssl is required")


def _make_cert(directory: Path, common_name: str) -> str:
  key, cert = directory / "k.pem", directory / "c.pem"
  subprocess_run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1", "-subj", f"/CN={common_name}", "-keyout", str(key), "-out", str(cert)], check=True, capture_output=True)
  return cert.read_text()


def test_filter_removes_only_distrusted_certs(tmp_path):
  distrusted = _make_cert(tmp_path, "emSign Root CA - G1")
  other = _make_cert(tmp_path, "Some Other Root CA")
  bundle = tmp_path / "bundle.pem"
  bundle.write_text(distrusted + other)

  subprocess_run([str(SCRIPT), "filter", str(bundle)], check=True, capture_output=True)

  assert bundle.read_text().strip() == other.strip()


def test_filter_handles_certifi_style_bundles(tmp_path):
  # certifi (used by pip and requests) and uv's bundled roots are PEM bundles with comment headers
  distrusted = _make_cert(tmp_path, "emSign ECC Root CA - G3")
  other = _make_cert(tmp_path, "Some Other Root CA")
  bundle = tmp_path / "cacert.pem"
  bundle.write_text(f"# Issuer: CN=emSign ECC Root CA - G3\n{distrusted}\n# Issuer: CN=Some Other Root CA\n{other}")

  subprocess_run([str(SCRIPT), "filter", str(bundle)], check=True, capture_output=True)

  assert "emSign" not in bundle.read_text()
  assert other.strip() in bundle.read_text()


def test_env_points_uv_and_pip_at_system_store(tmp_path):
  github_env = tmp_path / "github_env"
  github_env.touch()
  subprocess_run([str(SCRIPT), "env"], check=True, capture_output=True, env={**os_environ, "GITHUB_ENV": str(github_env)})

  exported = github_env.read_text().splitlines()
  assert "UV_NATIVE_TLS=true" in exported
  assert any(line.startswith("SSL_CERT_FILE=") for line in exported)
  assert any(line.startswith("PIP_CERT=") for line in exported)


@pytest_mark.skipif(not os_environ.get("CI"), reason="only enforced in CI")
def test_ci_trust_stores_do_not_trust_distrusted_certs():
  result = subprocess_run([str(SCRIPT), "verify"], capture_output=True, text=True)
  assert result.returncode == 0, result.stdout + result.stderr
