from os import environ as os_environ
from pathlib import Path
from shutil import which as shutil_which
from subprocess import CompletedProcess
from subprocess import run as subprocess_run

from pytest import mark as pytest_mark

SCRIPT = Path(__file__).resolve().parents[2] / "bin" / "lockdown"
IN_CI = bool(os_environ.get("CI"))

requires_openssl = pytest_mark.skipif(shutil_which("openssl") is None, reason="openssl is required")
ci_only = pytest_mark.skipif(not IN_CI, reason="only enforced in CI")

# Never touch the real stores from a test unless explicitly asked to
ISOLATED_ENV = {"SYSTEM_BUNDLE": "/nonexistent/system.crt", "PYTHON_BUNDLE_ROOTS": "/nonexistent"}


def _lockdown(*args: str, **env: str) -> CompletedProcess:
  return subprocess_run([str(SCRIPT), *args], capture_output=True, text=True, env={**os_environ, **ISOLATED_ENV, **env})


def _make_cert(directory: Path, common_name: str) -> str:
  key, cert = directory / f"{common_name}.key", directory / f"{common_name}.pem"
  subprocess_run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1", "-subj", f"/CN={common_name}", "-keyout", str(key), "-out", str(cert)], check=True, capture_output=True)
  return cert.read_text()


@requires_openssl
def test_filter_removes_only_distrusted_certs(tmp_path):
  distrusted = _make_cert(tmp_path, "emSign Root CA - G1")
  other = _make_cert(tmp_path, "Some Other Root CA")
  bundle = tmp_path / "bundle.pem"
  bundle.write_text(distrusted + other)

  assert _lockdown("filter", str(bundle)).returncode == 0

  assert bundle.read_text().strip() == other.strip()


@requires_openssl
def test_filter_removes_comodo_aaa_root(tmp_path):
  distrusted = _make_cert(tmp_path, "AAA Certificate Services")
  other = _make_cert(tmp_path, "Some Other Root CA")
  bundle = tmp_path / "bundle.pem"
  bundle.write_text(distrusted + other)

  _lockdown("filter", str(bundle))

  assert bundle.read_text().strip() == other.strip()


@requires_openssl
def test_check_flags_system_bundle_that_trusts_distrusted_certs(tmp_path):
  bundle = tmp_path / "ca-certificates.crt"
  bundle.write_text(_make_cert(tmp_path, "emSign ECC Root CA - G3"))

  result = _lockdown("check", SYSTEM_BUNDLE=str(bundle))

  assert result.returncode != 0
  assert "system" in result.stdout and "STILL TRUSTS" in result.stdout


@requires_openssl
def test_check_passes_clean_system_bundle(tmp_path):
  bundle = tmp_path / "ca-certificates.crt"
  bundle.write_text(_make_cert(tmp_path, "Some Other Root CA"))

  assert _lockdown("check", SYSTEM_BUNDLE=str(bundle)).returncode == 0


@requires_openssl
def test_check_flags_and_filters_python_certifi_bundles(tmp_path):
  # certifi (used by pip/requests, including pip's vendored copy) bundles carry comment headers
  site_packages = tmp_path / "venv" / "lib" / "site-packages" / "pip" / "_vendor" / "certifi"
  site_packages.mkdir(parents=True)
  other = _make_cert(tmp_path, "Some Other Root CA")
  bundle = site_packages / "cacert.pem"
  bundle.write_text(f"# Issuer: CN=emSign ECC Root CA - G3\n{_make_cert(tmp_path, 'emSign ECC Root CA - G3')}\n# Issuer: CN=Some Other Root CA\n{other}")
  roots = {"PYTHON_BUNDLE_ROOTS": str(tmp_path / "venv")}

  assert _lockdown("check", **roots).returncode != 0

  assert _lockdown("filter", str(bundle)).returncode == 0
  assert "emSign" not in bundle.read_text()
  assert other.strip() in bundle.read_text()
  assert _lockdown("check", **roots).returncode == 0


def test_env_points_uv_and_pip_at_system_store(tmp_path):
  github_env = tmp_path / "github_env"
  github_env.touch()

  assert _lockdown("env", GITHUB_ENV=str(github_env)).returncode == 0

  exported = github_env.read_text().splitlines()
  assert "UV_SYSTEM_CERTS=true" in exported
  assert any(line.startswith("SSL_CERT_FILE=") for line in exported)
  assert any(line.startswith("PIP_CERT=") for line in exported)


# The tests below run against the real stores, after bin/lockdown has been applied by the workflow
@ci_only
def test_ci_trust_stores_do_not_trust_distrusted_certs():
  result = subprocess_run([str(SCRIPT), "check"], capture_output=True, text=True, env={k: v for k, v in os_environ.items() if k not in ISOLATED_ENV})
  assert result.returncode == 0, result.stdout + result.stderr


@ci_only
def test_ci_live_probes_reject_compromised_intermediates():
  result = subprocess_run([str(SCRIPT), "verify"], capture_output=True, text=True, env={k: v for k, v in os_environ.items() if k not in ISOLATED_ENV})
  assert result.returncode == 0, result.stdout + result.stderr
