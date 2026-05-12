# Changelog

All notable changes to QiloBack are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file tracks the **public wrapper** release line — the npm package `@qiloback/qiloback`, the PyPI package `qiloback-cli`, and the binaries attached to GitHub Releases. Internal generator changes that ship in the same tag are summarised here at release time.

## [Unreleased]

## [0.3.4] — 2026-05-11

### Added

- CLI parity with the panel — ten new sub-trees so every surface the
  panel renders is also reachable from the terminal: `secrets`,
  `cron`, `webhooks`, `channels`, `edge-functions`, `storage`,
  `auth-config`, `members`, `domains`, `logs`. All owner-scoped
  through the platform-api.
- Interactive TUI rebuild — running `qiloback` with no args opens
  the terminal UI with six sections (Sesión, Workspace, Build,
  Project, Deploy, Ops) and 25+ actions.
- Per-command `--help` examples and shell completions for bash /
  zsh / fish via `qiloback completions install`.

### Notes

- The binary tagged `v0.3.4` carries the new sub-trees + TUI. PyPI
  + npm package versions are pinned to the same `0.3.4` tag.

## [0.3.3] — 2026-05-09

### Changed

- npm scope flipped from `@delixon` to `@qiloback`. The package is now `@qiloback/qiloback`. The PyPI package name (`qiloback-cli`) and the binary download surface are unchanged.
- README, CHANGELOG, the npm-publish workflow and the dependabot configuration updated to reference the new scope.

### Notes

- The 0.3.0–0.3.2 tags in `delixon-labs/qiloback-core` were cut while the public-wrapper publish path was being prepared; 0.3.3 is the first version that publishes from this repository to npm and PyPI.

## [0.3.0] — Unreleased

The initial release cut from the new public wrapper repository — never published, superseded by 0.3.3.

### Added

- npm wrapper `@qiloback/qiloback` — downloads and verifies the `qiloback` binary on first install, caches it under `~/.qiloback/bin/`, exposes `qiloback` and `qb` aliases.
- pip wrapper `qiloback-cli` — same flow as the npm wrapper, written in stdlib-only Python (no third-party runtime deps for the wrapper itself).
- `SHA256SUMS` verification on first install for both wrappers; mismatch deletes the partial download and aborts.
- `QILOBACK_BINARY` and `QILOBACK_SKIP_POSTINSTALL` environment variables for development against unreleased builds and offline installs.
- GitHub Releases assets per platform: `qiloback-cli-{win32,linux,darwin}-{x64,arm64}` plus the `SHA256SUMS` index.
- OIDC trusted publishing for both `@qiloback/qiloback` (npm) and `qiloback-cli` (PyPI). No long-lived registry tokens are stored in repository secrets.

### Security

- Wrapper postinstall scripts download via HTTPS only, follow up to 5 redirects, retry transient failures up to 3 times with backoff, and require a successful SHA-256 check (or an explicit forward-compatibility warning when `SHA256SUMS` is absent in older releases).
- Repository ships with a gitleaks allowlist (`.gitleaks.toml` in the core repository) pinned to audited fixture paths and explicit regexes; the public wrapper repo carries no runtime credentials.

[Unreleased]: https://github.com/delixon-labs/delixon-qiloback/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.3.0
