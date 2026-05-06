# Changelog

All notable changes to QiloBack are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file tracks the **public wrapper** release line — the npm package `@delixon/qiloback`, the PyPI package `qiloback-cli`, and the binaries attached to GitHub Releases. Internal generator changes that ship in the same tag are summarised here at release time.

## [Unreleased]

### Changed

- Public wrapper repository created at `delixon-labs/delixon-qiloback`. The npm and pip CLI wrappers, the user-facing documentation, the license and the compliance files now live here. The generator and platform sources remain in `delixon-labs/qiloback-core` (private) under the FSL window.
- Wrapper README, CONTRIBUTING and SECURITY files updated to reflect the split-repository layout. Installation commands (`npm install -g @delixon/qiloback`, `pip install qiloback-cli`) are unchanged.

## [0.3.0] — Unreleased

The first release cut from the new public wrapper repository.

### Added

- npm wrapper `@delixon/qiloback` — downloads and verifies the `qiloback` binary on first install, caches it under `~/.qiloback/bin/`, exposes `qiloback` and `qb` aliases.
- pip wrapper `qiloback-cli` — same flow as the npm wrapper, written in stdlib-only Python (no third-party runtime deps for the wrapper itself).
- `SHA256SUMS` verification on first install for both wrappers; mismatch deletes the partial download and aborts.
- `QILOBACK_BINARY` and `QILOBACK_SKIP_POSTINSTALL` environment variables for development against unreleased builds and offline installs.
- GitHub Releases assets per platform: `qiloback-cli-{win32,linux,darwin}-{x64,arm64}` plus the `SHA256SUMS` index.
- OIDC trusted publishing for both `@delixon/qiloback` (npm) and `qiloback-cli` (PyPI). No long-lived registry tokens are stored in repository secrets.

### Security

- Wrapper postinstall scripts download via HTTPS only, follow up to 5 redirects, retry transient failures up to 3 times with backoff, and require a successful SHA-256 check (or an explicit forward-compatibility warning when `SHA256SUMS` is absent in older releases).
- Repository ships with a gitleaks allowlist (`.gitleaks.toml` in the core repository) pinned to audited fixture paths and explicit regexes; the public wrapper repo carries no runtime credentials.

[Unreleased]: https://github.com/delixon-labs/delixon-qiloback/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.3.0
