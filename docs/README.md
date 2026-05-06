# Documentation

User-facing documentation for QiloBack lives in this folder as it stabilises. During the FSL window, the canonical references for the DSL grammar, the generator pipeline and the runtime APIs are kept in the private core repository (`delixon-labs/qiloback-core/docs/`) and released alongside each tagged version.

For now, the main entry points are:

- [README.md](../README.md) — installation, usage overview, and project information.
- [CHANGELOG.md](../CHANGELOG.md) — version history and release notes.
- [LICENSE](../LICENSE) and [LICENSE-FAQ.md](../LICENSE-FAQ.md) — license text and frequently asked questions.
- [SECURITY.md](../SECURITY.md) — how to report security vulnerabilities.
- [CONTRIBUTING.md](../CONTRIBUTING.md) — how to contribute.

The CLI itself ships with self-documenting help:

```bash
qiloback --help
qiloback init --help
qiloback generate --help
qiloback eject --help
```

Detailed guides — DSL reference, module catalogue, RLS recipes, deployment runbooks — will be added here over time and become public on the same cadence as the FSL → Apache 2.0 conversion of each release.
