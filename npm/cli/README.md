# @delixon/qiloback

QiloBack CLI distributed via npm. Wraps the native `qiloback` binary
published in GitHub Releases.

## Install

```bash
npm install -g @delixon/qiloback
qiloback --version
```

Or one-shot:

```bash
npx @delixon/qiloback init my-app
```

## How it works

`postinstall` detects your platform (`win32-x64`, `linux-x64`,
`linux-arm64`, `darwin-x64`, `darwin-arm64`), downloads the matching
binary from
`https://github.com/delixon-labs/delixon-qiloback/releases/download/v<X.Y.Z>/`,
verifies its sha256 against `SHA256SUMS`, and places it under `bin/`.

The `bin/qiloback` shim execs the binary with your args and stdio.

Set `NPM_QILOBACK_SKIP_POSTINSTALL=1` to skip the download (useful in
hermetic CI runners that pre-bake the binary).

## License

Source-available under FSL-1.1-ALv2 — see `LICENSE`.
