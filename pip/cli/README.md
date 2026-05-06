# qiloback-cli (pip wrapper)

QiloBack CLI distributed on PyPI. Wraps the native `qiloback` binary
published in GitHub Releases.

## Install

```bash
pip install --user qiloback-cli
qiloback --version
```

## How it works

On first invocation the wrapper:

1. Maps your host (Windows x64, Linux x64/arm64, macOS x64/arm64) to
   the matching release asset.
2. Fetches it from
   `https://github.com/delixon-labs/delixon-qiloback/releases/download/v<X.Y.Z>/`
   with retries and a 60 s timeout per attempt.
3. Verifies its sha256 against the release's `SHA256SUMS`.
4. Caches it under `~/.qiloback/bin/` and `chmod +x`'s it on Unix.

Subsequent calls reuse the cached binary.

Override the binary location with `QILOBACK_BINARY=/path/to/qiloback`
during development against an unreleased build.

## License

Source-available under FSL-1.1-ALv2 — see `LICENSE`.
