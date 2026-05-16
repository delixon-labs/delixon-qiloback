"""QiloBack CLI wrapper — downloads and execs the native binary.

The ``qiloback`` binary lives in GitHub Releases, one per platform.
On first invocation we map the host (system + machine) to a release
asset, fetch it with retries, verify the sha256 against the
``SHA256SUMS`` file shipped alongside, ``chmod +x`` it on Unix, and
cache it under ``~/.qiloback/bin/``. Subsequent calls reuse the
cached binary.

Set ``QILOBACK_BINARY`` to point at a local binary you control —
useful for development against an unreleased build.
"""

from __future__ import annotations

import hashlib
import os
import platform
import subprocess
import sys
import time
import urllib.error
import urllib.request
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from pathlib import Path

_DOWNLOAD_TIMEOUT_S = 60
_DOWNLOAD_MAX_RETRIES = 3
_DOWNLOAD_RETRY_DELAY_S = 2

_PLATFORM_MAP: dict[tuple[str, str], str] = {
    ("Windows", "AMD64"): "qiloback-cli-win32-x64.exe",
    ("Windows", "x86_64"): "qiloback-cli-win32-x64.exe",
    ("Linux", "x86_64"): "qiloback-cli-linux-x64",
    ("Linux", "aarch64"): "qiloback-cli-linux-arm64",
    ("Darwin", "x86_64"): "qiloback-cli-darwin-x64",
    ("Darwin", "arm64"): "qiloback-cli-darwin-arm64",
}


def _resolve_version() -> str:
    """Read the version from package metadata; fall back to 0.0.0 only
    when the package is not installed (developer mode)."""
    try:
        return _pkg_version("qiloback-cli")
    except PackageNotFoundError:
        return "0.0.0"


__version__ = _resolve_version()
_RELEASE_BASE = "https://github.com/delixon-labs/delixon-qiloback/releases/download/v{version}"


def _bin_dir() -> Path:
    target = Path.home() / ".qiloback" / "bin"
    target.mkdir(parents=True, exist_ok=True)
    return target


def _binary_asset() -> str:
    system = platform.system()
    machine = platform.machine()
    asset = _PLATFORM_MAP.get((system, machine))
    if asset is None:
        print(
            f"qiloback-cli: unsupported platform ({system} / {machine})",
            file=sys.stderr,
        )
        print(
            "Supported: Windows x64, Linux x64/arm64, macOS x64/arm64",
            file=sys.stderr,
        )
        sys.exit(1)
    return asset


def _binary_path() -> Path:
    name = "qiloback.exe" if platform.system() == "Windows" else "qiloback"
    return _bin_dir() / name


def _http_get(url: str, *, timeout: int = _DOWNLOAD_TIMEOUT_S) -> bytes | None:
    """GET with retries and timeout. Returns bytes, or None on 404."""
    last_err: Exception | None = None
    for attempt in range(1, _DOWNLOAD_MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(url, timeout=timeout) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            last_err = exc
        except (urllib.error.URLError, TimeoutError) as exc:
            last_err = exc
        if attempt < _DOWNLOAD_MAX_RETRIES:
            time.sleep(_DOWNLOAD_RETRY_DELAY_S)
    raise RuntimeError(f"failed fetching {url}: {last_err}") from last_err


def _expected_sha(asset: str, version: str) -> str | None:
    """Look up the expected sha256 for ``asset`` from the release's
    ``SHA256SUMS`` file. Returns ``None`` when the file is missing
    (older release without checksums)."""
    text = _http_get(_RELEASE_BASE.format(version=version) + "/SHA256SUMS")
    if text is None:
        return None
    for raw in text.decode("utf-8", errors="replace").splitlines():
        line = raw.strip()
        if not line or not line.endswith(asset):
            continue
        return line.split()[0].lower()
    return None


def _ensure_binary() -> Path:
    """Make sure the native binary is on disk and return its path."""
    override = os.environ.get("QILOBACK_BINARY")
    if override:
        path = Path(override).expanduser()
        if not path.exists():
            print(
                f"qiloback-cli: QILOBACK_BINARY points at a missing file: {path}",
                file=sys.stderr,
            )
            sys.exit(1)
        return path

    target = _binary_path()
    if target.exists() and target.stat().st_size > 0:
        return target

    asset = _binary_asset()
    version = __version__
    if version == "0.0.0":
        print(
            "qiloback-cli: cannot resolve package version — install via pip first.",
            file=sys.stderr,
        )
        sys.exit(1)
    download_url = f"{_RELEASE_BASE.format(version=version)}/{asset}"

    payload = _http_get(download_url)
    if payload is None:
        print(
            f"qiloback-cli: asset not found: {download_url}",
            file=sys.stderr,
        )
        sys.exit(1)

    expected = _expected_sha(asset, version)
    if expected:
        actual = hashlib.sha256(payload).hexdigest()
        if actual.lower() != expected.lower():
            print(
                f"qiloback-cli: sha256 mismatch — expected {expected}, got {actual}",
                file=sys.stderr,
            )
            sys.exit(2)

    target.write_bytes(payload)
    if platform.system() != "Windows":
        target.chmod(0o755)
    return target


def main() -> None:
    """Entry point: lazy-fetch the binary, then exec it with argv.

    Exports ``QILOBACK_INSTALL_CHANNEL=pip`` so the binary's update
    detector can pick the right upgrade command (``pip install
    --upgrade``) instead of falling back to the generic GitHub
    download path. The wrapper is the only side that knows for sure
    how the user installed the CLI."""
    binary = _ensure_binary()
    env = os.environ.copy()
    env.setdefault("QILOBACK_INSTALL_CHANNEL", "pip")
    completed = subprocess.run([str(binary), *sys.argv[1:]], check=False, env=env)
    sys.exit(completed.returncode)


if __name__ == "__main__":
    main()
