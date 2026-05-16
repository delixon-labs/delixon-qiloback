# Changelog

All notable changes to QiloBack are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This file tracks the **public wrapper** release line — the npm package `@qiloback/qiloback`, the PyPI package `qiloback-cli`, and the binaries attached to GitHub Releases. Internal generator changes that ship in the same tag are summarised here at release time.

## [Unreleased]

## [0.5.0] — 2026-05-15

Lockstep bump with `delixon-labs/qiloback-core` v0.5.0. The
core release brings the Live Backend (dual-mode runtime, hot
apply, destructive-op flow with five-minute undo, Dev/Prod
parity gate), self-hosted frontend hosting via the new
``qiloback`` provider, the developer plan + ``qb_test_…``
long-lived tokens for SDK / CI / partner integrations, and the
seven audit-driven fixes (eject backend boots end-to-end via
``docker compose``, Caddy custom-domain pipeline, runtime path
rewrite, lifetime project quota, AI Builder sandbox + Ollama,
``QILOBACK_GENERATED_DIR`` empty-string guard). Detail in the
core CHANGELOG.

### Changed

- npm: `@qiloback/qiloback` 0.3.11 → 0.5.0.
- PyPI: `qiloback-cli` 0.3.11 → 0.5.0.
- Both wrappers download the matching `v0.5.0` binaries from
  GitHub Releases on first install and verify them against
  the published `SHA256SUMS`.

## [0.3.11] — 2026-05-13

### Fixed

- **No more 409 on project creation.** Lockstep with the core
  release: POST /api/v1/projects now auto-suffixes the
  slug (slug-2, slug-3…) instead of rejecting the
  request when the requested slug is already taken globally.
- **Drag-and-drop folder ingest works in the panel.** Dropping
  a folder onto the ingest drop zone now routes to
  /ingest/upload-folder instead of trying to ship it as a
  zip to /ingest/upload and getting a 400. Archive drops
  still flow through /ingest/upload unchanged.

### Notes

- All distribution surfaces ship at 0.3.11 together: npm
  (4 packages), PyPI (3 packages), VS Code Marketplace, Open
  VSX, Helm chart, the GitHub Release with the signed CLI /
  Rust binaries.

## [0.3.10] — 2026-05-13

### Security

- Lockstep bump with ``delixon-labs/qiloback-core`` v0.3.10.
  The core release closes 43 of 45 Dependabot alerts left open
  at v0.3.9 — Next 14 → 15 + React 18 → 19 plus the Python deps
  (Mako, urllib3, python-multipart). Wrapper itself carries no
  third-party runtime deps, so this release just re-pins the
  binary download URL + the PyPI/npm wrapper manifests.

### Fixed

- Three regressions that hid in the v0.3.9 binaries (validation
  422 → 500 with no CORS, RUM ingest crashing on
  ``meter.increment(...)``, ``telemetry/events?kind=rum``
  returning empty after a successful POST) are all fixed in the
  core repo; the v0.3.10 binaries this wrapper downloads carry
  the patches.

### Notes

- ``Publish npm`` and ``Publish pip`` workflows on this repo
  are idempotent now — re-dispatching a tag's publish run no
  longer fails with ``"version not changed"`` or
  ``"E403 cannot publish"``.

## [0.3.9] — 2026-05-12

### Added

- **Sprint 9 surface in the CLI.** The `qiloback` binary tagged
  `v0.3.9` ships every Sprint 9 endpoint reachable from the
  terminal: per-project staging environments (`qiloback env list /
  create / deploy / archive`), self-service backups (`qiloback
  backup trigger / list / download`), webhook deliveries +
  retry policy editor, and the per-project typed SDK builder
  (`qiloback sdk build {ts|py|dart|go|swift}`).
- **Nexenv interop.** New sub-commands wire the CLI to the local
  Nexenv engine when one is attached: `qiloback nexenv
  handshake / hint`, plus `qiloback generate --stream` for the
  Server-Sent Events generation stream.
- **Storage cap + monthly egress in `qiloback quota`.** The four
  free-tier counters (projects, daily_requests, database_bytes,
  monthly_egress_bytes) now render with severity bars so the
  CLI matches the panel's overage banner.

### Fixed (production hardening)

- POST `/projects` no longer returns 500 on a slug race —
  `IntegrityError` is mapped to a 409 Conflict with a CORS
  envelope so the panel surfaces a usable message instead of
  a NetworkError cascade.
- Runtime URL surface — generated projects now expose
  `https://runtime.qiloback.dev/p/{slug}/api/v1` (the control
  plane lived on `api.qiloback.dev`; the prior wrapper pointed
  the deploy CTA at the wrong host).
- Generated projects with slugs containing hyphens (e.g.
  `mi-tienda`) load correctly — the runtime mounter now
  translates the slug to a valid Python module name before
  importing.
- Codegen emits `requirements.txt` alongside `pyproject.toml`
  so legacy buildpacks (Render, Heroku, certain CI cache
  layers) read the dependency list without a PEP 621 parser.
- Ingest endpoints fall back to writable storage paths
  (`/var/lib/qiloback/ingest` → `/tmp/qiloback/ingest`) when
  the container's working directory is read-only.

### Changed

- **Package manager.** The workspace has moved off npm onto
  pnpm 11. CI runners, the admin-panel Docker image and the
  release-package-managers workflow all target Node 22 + pnpm
  11 in lockstep. Documented in the core repo's
  `~/.config/pnpm/config.yaml` and reflected here for users
  building from the monorepo.

### Notes

- All distribution surfaces ship at `0.3.9` together: npm
  (`@qiloback/qiloback`, `@qiloback/sdk`, `@qiloback/qiloback-mcp`,
  `@qiloback/claude-code-qiloback`), PyPI (`qiloback-cli`,
  `qiloback-mcp`, `qiloback-sdk`), VS Code Marketplace
  (`delixon-labs.qiloback-dsl`), Open VSX, Helm chart, and 27
  signed CLI / Rust binaries attached to the GitHub Release.

## [0.3.8] — 2026-05-12

### Added

- npm + PyPI publish wrappers in this public repository now run
  on every `v*` tag pushed from `delixon-labs/qiloback-core`,
  so a release no longer requires a manual `pnpm publish` step.
- Dependabot disabled in the wrapper repo (the wrappers carry
  no runtime third-party deps); the core repo is the single
  authoritative dependency surface.

## [0.3.7] — 2026-05-11

### Added

- Sprint 8 ingest hardening reflected in the CLI — `qiloback
  ingest upload` honours the per-project quota, surfaces the
  storage cap, and retries 5xx with exponential backoff.

## [0.3.6] — 2026-05-11

### Added

- Internal release infrastructure: SLSA-style provenance
  attached to every GitHub Release asset; sigstore signatures
  cover the cross-platform CLI binaries.

## [0.3.5] — 2026-05-11

### Added

- Cross-platform CLI binaries (`linux-x64`, `linux-arm64`,
  `darwin-arm64`, `win32-x64.exe`) attached to the GitHub
  Release. Wrapper postinstall downloads the right one based
  on `process.platform` + `process.arch`.

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

[0.5.0]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.5.0
[Unreleased]: https://github.com/delixon-labs/delixon-qiloback/compare/v0.3.11...HEAD
[0.3.11]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.3.11
[0.3.10]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.3.10
[0.3.9]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.3.9
[0.3.8]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.3.8
[0.3.7]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.3.7
[0.3.6]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.3.6
[0.3.5]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.3.5
[0.3.4]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.3.4
[0.3.3]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.3.3
[0.3.0]: https://github.com/delixon-labs/delixon-qiloback/releases/tag/v0.3.0
