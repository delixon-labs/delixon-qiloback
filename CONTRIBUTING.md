# Contributing to QiloBack

Thanks for your interest in contributing to QiloBack.

QiloBack is a product of [Delixon Labs](https://delixon.dev), the developer tools division of [XPlus Technologies LLC](https://xplustechnologies.com). It is licensed under [FSL-1.1-ALv2](LICENSE) — source-available, not open source. Each version converts to Apache 2.0 two years after its release.

Before contributing, please read this document in full.

---

## Where does the code live?

QiloBack is split across two repositories:

- **This repository** (`delixon-labs/delixon-qiloback`, public) hosts the installation wrappers (`npm/cli/`, `pip/cli/`), the user-facing documentation (`docs/`), the license, and the compliance files (SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, CHANGELOG.md). Pull requests to these areas are open and welcome.
- **`delixon-labs/qiloback-core`** (private) hosts the generator (DSL → FastAPI), the platform API, the runtime API, the admin panel, the SDKs, the release pipelines and the deployment manifests. The source code is not publicly browsable during each version's first two years (the FSL window). Two years after each release that version becomes Apache 2.0 and its source becomes public.

To contribute to the **core**, follow the invited-access flow in the next section. For everything else (wrappers, docs, compliance files), open a PR directly in this repository.

---

## Before you start

### License and contributions

QiloBack is **source-available**, not open source. By contributing code, documentation, or other materials to this project, you agree that your contribution is licensed under the same terms as the rest of the project (FSL-1.1-ALv2 with conversion to Apache 2.0 two years after each version's release).

For non-trivial contributions, we may ask you to sign a Contributor License Agreement (CLA) before merging. This is a lightweight agreement that confirms you have the right to contribute the code and grants us the necessary license to include it. We will send you the CLA when your PR reaches that point.

### Code of conduct

All contributors are expected to follow the [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful, constructive, and focused on the work.

---

## What kind of contributions are welcome

### ✅ Welcome in this public repository

- **Bug reports** against QiloBack (reproduction steps, OS + version, error output, the `qiloback.yml` that triggers it when relevant)
- **Fixes and improvements to the npm wrapper** (`npm/cli/`)
- **Fixes and improvements to the pip wrapper** (`pip/cli/`)
- **Documentation improvements** (`docs/`, README, CONTRIBUTING, LICENSE-FAQ)
- **Typo fixes** and small polish PRs
- **Translations** of user-facing documentation

### ✅ Welcome in the core — through the invited-access flow

- **Bug fixes** to the generator, platform API, runtime API or admin panel
- **New first-party modules** (auth strategy, billing provider, search backend, storage adapter, etc.)
- **New project templates** under `templates/`
- **Performance improvements** with benchmarks against the existing baseline
- **Generator improvements** that reduce the gap between the DSL and what production-grade FastAPI services need

### ⚠️ Discuss first (open an issue in this repository)

- **New CLI commands** or major surface changes
- **Breaking changes** to the DSL grammar or to a generated artefact's contract
- **New core features** not already on the roadmap
- **Large refactors** of the generator pipeline or the admin panel
- **Changes to the security audit, RLS or audit-log generators** — these surfaces affect every generated backend
- **Additions to the CI/release pipeline**

### ❌ Not welcome

- Contributions that modify the license or its enforcement
- Changes that weaken row-level security, audit logging or secret-handling defaults
- Telemetry or tracking added without explicit opt-in design
- Commercial-competitor adaptations (prohibited by license)
- Security vulnerability reports in PRs (see [SECURITY.md](SECURITY.md))
- AI-generated code dropped without disclosure or review

---

## How to contribute

### Contributing to the wrappers or documentation (public)

1. **Find or create an issue** in [this repository's issue tracker](https://github.com/delixon-labs/delixon-qiloback/issues). For small fixes (typos, clear bugs), feel free to open a PR directly.
2. **Fork and branch**

   ```bash
   git clone https://github.com/YOUR-USERNAME/delixon-qiloback.git
   cd delixon-qiloback
   git checkout -b fix/description-of-change
   ```

3. **Make your changes** in `npm/cli/`, `pip/cli/`, or the root documentation files.
4. **Test the wrappers** locally:

   ```bash
   # pip wrapper
   pip install --user --editable pip/cli
   qiloback --version

   # npm wrapper
   cd npm/cli && npm install
   ./bin/qiloback --version
   ```

5. **Open a PR against the `dev` branch** with a clear title and description.

### Contributing to the core (private repository)

1. **Open an issue in this public repository** describing what you would like to change. Link to the relevant DSL surface, the affected generated artefact, or the bug reproduction.
2. If the change is welcome and non-trivial, we will reply with next steps: CLA (where applicable) and temporary access to `delixon-labs/qiloback-core` for your specific contribution.
3. Your PR is opened in the private repository and merged under FSL-1.1-ALv2 like the rest of the project.
4. The resulting release is cut from the private repository and the binaries are published in this public repository's [Releases](https://github.com/delixon-labs/delixon-qiloback/releases) on the next tag.

For small bug fixes and suggestions, opening an issue here is always the fastest path.

### Review process

- A maintainer will review within ~7 days for most PRs.
- We may ask for changes or discuss alternative approaches.
- Once approved, a maintainer will merge and include the change in the next release.

---

## Branching and releases

The public repository uses a three-branch model:

```
feature/* or fix/*  →  local  →  dev  →  main
```

- `local`: day-to-day work, fast-moving.
- `dev`: integration branch before release.
- `main`: tracks the latest stable release (tagged).

Contributors should open PRs against `dev`. Direct pushes to `main`, `dev` and `local` are blocked by branch protection on plans where it is available — including for maintainers (`enforce_admins: true`). Merging to `main` is restricted to repository owners.

Releases are cut by maintainers from the private core repository. The release workflow builds the binaries in `qiloback-core` and publishes them as assets on a tagged release here, alongside `SHA256SUMS` for integrity verification. The npm and pip wrappers in this repository are then bumped to the same version and published via OIDC trusted publishing — no long-lived registry tokens involved.

---

## Reporting bugs

Before opening an issue:

1. Search existing issues.
2. Reproduce with the latest version (`qiloback --version` to check).
3. Collect: OS + version, QiloBack version, full error output, minimal `qiloback.yml` reproduction (when the bug is DSL-driven), and the generator command you ran.

Issue templates will guide you through this.

---

## Requesting features

Open an issue with:

- The problem you are trying to solve (the *why*).
- How you currently work around it.
- Your proposed solution (if any).
- Why this fits QiloBack's scope ("backend manufacturer — DSL to production-grade FastAPI service").

Features that don't fit QiloBack's scope will be declined respectfully.

---

## What not to do

- Don't submit PRs for unrelated changes (one topic per PR).
- Don't change the license or remove copyright notices.
- Don't add dependencies without discussion — we keep the dep graph tight on both Python and TypeScript sides.
- Don't submit AI-generated code without review — disclose it in the PR description so we can review with appropriate scrutiny.
- Don't report security issues publicly (see [SECURITY.md](SECURITY.md)).
- Don't commit fixtures that contain real credentials. The repository ships a gitleaks allowlist for known-safe fixtures; new fixtures must keep entropy below the scanner thresholds or extend the allowlist with a justification.

---

## Getting help

- **Bug reports and feature requests:** [GitHub Issues](https://github.com/delixon-labs/delixon-qiloback/issues)
- **Security issues:** see [SECURITY.md](SECURITY.md) — never report vulnerabilities via public issues
- **Licensing questions, code audits under NDA, core contribution requests:** see [LICENSE-FAQ.md](LICENSE-FAQ.md) or email `legal@delixon.dev`
- **Commercial inquiries:** `hello@delixon.dev`

---

## Recognition

Contributors are credited in release notes. For significant contributions, you will be listed in a `CONTRIBUTORS.md` (coming).

Thank you for helping make QiloBack better.
