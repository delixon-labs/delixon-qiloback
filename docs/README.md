# Documentation

User-facing documentation for QiloBack lives in this folder as it
stabilises. During the FSL window, the canonical references for the
DSL grammar, the generator pipeline and the runtime APIs are kept in
the private core repository (`delixon-labs/qiloback-core/docs/`) and
released alongside each tagged version.

## Public guides

- **[Getting started](getting-started.md)** — every install path, what each one gives you, the 26 CLI commands, the typical first-time flow.

## Project documents

- [README](../README.md) — installation snapshot, usage overview, project information.
- [CHANGELOG](../CHANGELOG.md) — version history and release notes.
- [LICENSE](../LICENSE) and [LICENSE-FAQ](../LICENSE-FAQ.md) — license text and frequently asked questions.
- [SECURITY](../SECURITY.md) — how to report a vulnerability.
- [CONTRIBUTING](../CONTRIBUTING.md) — how to contribute.
- [CODE_OF_CONDUCT](../CODE_OF_CONDUCT.md) — community standards.

## Self-documenting CLI

The CLI ships with a help system on every subcommand:

```bash
qiloback --help
qiloback init --help
qiloback generate --help
qiloback eject --help
```

Detailed guides — DSL reference, module catalogue, RLS recipes,
deployment runbooks — land here on the same cadence as each tagged
release converts from FSL to Apache 2.0.
