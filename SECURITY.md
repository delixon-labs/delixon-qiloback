# Security Policy

## Reporting a vulnerability

If you discover a security vulnerability in QiloBack, please report it
responsibly. **Do not open a public GitHub issue.**

### Contact

- **Email:** `security@delixon.dev`
- **GitHub Security Advisory:** [Report privately](https://github.com/delixon-labs/delixon-qiloback/security/advisories/new)

Include the following in your report:

- Description of the vulnerability
- Steps to reproduce (proof of concept if available)
- Affected version(s) (`qiloback --version`)
- Operating system and version
- Impact assessment (if known)
- Suggested fix (if any)
- Whether you have already disclosed this to anyone else

### Response timeline

| Stage              | Timeframe              |
|--------------------|------------------------|
| Acknowledgment     | Within 48 hours        |
| Initial assessment | Within 5 business days |
| Fix development    | Depends on severity    |
| Public disclosure  | After fix is released  |

### Severity classification

| Severity | Description                                            | Target fix time |
|----------|--------------------------------------------------------|-----------------|
| Critical | Remote code execution, auth bypass, data leak         | 72 hours        |
| High     | Privilege escalation, SQL injection, SSRF             | 7 days          |
| Medium   | XSS, CSRF, information disclosure                      | 30 days         |
| Low      | Hardening recommendations, best practices              | Next release    |

## Supported versions

| Version           | Supported |
|-------------------|-----------|
| `0.3.x` (current) | ✅ Yes    |
| `< 0.3.0`         | ❌ No     |

Only the latest minor release receives security patches. We recommend
always running the latest version. The
[Functional Source License](LICENSE) auto-converts each released
version to Apache 2.0 two years after its release; for the security
posture, pinning to the latest release is what matters.

## Scope

The following are considered in-scope for security reports:

- Arbitrary code execution via the QiloBack CLI or generator
- Vulnerabilities in the generated FastAPI templates that affect every
  generated backend (template-level CWEs)
- Authentication, authorization, or RLS bypass in the platform API
- Reading files outside the user's project directory during generation
- Leaking secrets, API keys or tokens through generated artefacts
- Supply-chain integrity of binaries and packages distributed via
  npm, PyPI, GitHub Releases or `ghcr.io`
- Memory-safety bugs in compiled binaries

The following are **out of scope**:

- Vulnerabilities in third-party dependencies (please report them
  upstream; we monitor advisories and update via Dependabot)
- Issues that require local physical access to an unlocked machine
- Social engineering or phishing
- Findings against an *eject*ed FastAPI codebase you have modified
  yourself — once ejected, the backend is yours under Apache 2.0 and
  outside QiloBack's responsibility

## Security practices

QiloBack is designed with these principles:

- **No silent telemetry** — the self-hosted control plane has no
  required cloud component; the hosted SaaS only processes what an
  account holder explicitly sends.
- **Reproducible binaries** — every release is built in CI from a
  tagged commit and accompanied by `SHA256SUMS`; npm and pip wrappers
  verify the checksum on first install.
- **Least privilege by default** — generated backends ship with RLS
  policies, audit logging and per-route role gates already wired.
- **Dependency hygiene** — Dependabot covers Python, npm, GitHub
  Actions and Docker base images on a weekly cadence; security PRs are
  unbounded.
- **Static analysis** — `ruff`, `mypy --strict`, `pip-audit`, `pnpm
  audit` and gitleaks run in CI; the secret scanner used by the
  generator (`packages/ingest`) doubles as a pre-commit hook for
  customer manifests.

## Disclosure timeline

We aim for **90 days** from report to public disclosure, with
flexibility depending on severity and complexity.

---

*Last updated: 2026-05-06*
