# Getting started

QiloBack ships across nine distribution channels. Pick whichever fits the
machine you are on; every channel installs the same `qiloback` binary
underneath.

> All commands below are real. Anything tagged with ⏳ is still being
> rolled out for the current release line and will become available on
> the next tag.

## Install

### CLI via npm

```bash
npm install -g @qiloback/qiloback
qiloback --version
```

The `postinstall` step downloads the matching native binary from the
[GitHub release](https://github.com/delixon-labs/delixon-qiloback/releases),
verifies the SHA-256 against the release's `SHA256SUMS`, and caches the
result under `~/.qiloback/bin/`. Subsequent calls reuse the cached binary;
no network hit, no Node startup overhead.

Exposes `qiloback` and `qb` (alias).

### CLI via pip

```bash
pip install --user qiloback-cli
qiloback --version
```

Same flow as the npm wrapper — written in stdlib-only Python so the
install works on any minimal CPython 3.10+ image without extra deps.

### CLI via direct binary download

```bash
curl -L https://github.com/delixon-labs/delixon-qiloback/releases/download/v0.3.3/qiloback-linux-x64 \
  -o qiloback
chmod +x qiloback
sudo mv qiloback /usr/local/bin/
qiloback --version
```

Useful in CI images that ship neither Node nor Python. Verify the binary
against `SHA256SUMS.txt` attached to the same release.

Available platforms: `linux-x64`, `linux-arm64`, `darwin-arm64`,
`win32-x64.exe`, plus `darwin-x64` ⏳.

### MCP server via npm or pip

```bash
npm install -g @qiloback/qiloback-mcp
# or
pip install qiloback-mcp
```

The MCP (Model Context Protocol) server lets AI tools (Claude, Cursor,
Windsurf, any MCP-aware client) call into a running QiloBack platform-api
through 32 typed tools — `create_project`, `update_dsl`, `validate_dsl`,
`generate_backend`, `eject_project`, etc. Configure your MCP client to
point at `qiloback-mcp` and it discovers the tools automatically.

### Claude Code skill

```bash
npm install -g @qiloback/claude-code-qiloback
```

Auto-loaded skill for [Claude Code](https://claude.com/claude-code). When
the conversation touches `qiloback.yml` or any of `init`, `validate`,
`generate`, `migrate`, `dev`, `eject`, or "AI Builder" prompts, Claude
prefers the typed MCP tools when an MCP server is wired and falls back
to the local CLI otherwise.

### VS Code / Cursor / Windsurf extension

- **VS Code Marketplace:** install [`delixon-labs.qiloback-dsl`](https://marketplace.visualstudio.com/items?itemName=delixon-labs.qiloback-dsl).
- **Open VSX (Cursor, Windsurf, VSCodium):** install
  [`delixon-labs/qiloback-dsl`](https://open-vsx.org/extension/delixon-labs/qiloback-dsl).

Adds the `qiloback-yaml` language for `qiloback.yml`/`*.qiloback.yaml`
files: TextMate grammar, snippets, JSON-schema validation against
`https://qiloback.dev/schema/v1.json` (autocomplete + linting in real
time), and a `Qiloback: Validate` command palette entry.

### Python SDK

```bash
pip install qiloback-sdk
```

Programmatic access to the platform-api from Python:

```python
from qiloback import Client

client = Client(base_url="https://api.example.com", api_key="...")
project = client.projects.create(name="My CRM", template="crm")
client.projects.update_dsl(project.id, yaml_text)
generation = client.projects.generate(project.id)
bundle = client.projects.eject(project.id)  # zip of the generated FastAPI source
```

Public surface: `Client`, `Project`, `GenerationLog`, `ValidationResult`,
`DSLDiff`, `EjectBundle`, plus the typed exception hierarchy
(`QiloBackError`, `APIError`, `AuthError`, `NotFoundError`,
`ValidationError`).

### Dart SDK ⏳

```bash
dart pub add qiloback
```

Same posture as the Python SDK, for Flutter / Dart apps:

```dart
import 'package:qiloback/qiloback.dart';

final client = QiloBackClient(
  baseUrl: 'https://api.example.com',
  apiKey: '...',
);
await client.projects.create(name: 'My CRM', template: 'crm');
```

Exposes `QiloBackClient`, `ProjectsApi`, `ComponentsApi`, `AuditApi`,
`EjectBundle`, and the error hierarchy. Pending its first publication on
[pub.dev](https://pub.dev/packages/qiloback).

### Self-host: Docker images

```bash
docker pull ghcr.io/delixon-labs/qiloback-platform-api:0.3.3
docker pull ghcr.io/delixon-labs/qiloback-runtime-api:0.3.3
docker pull ghcr.io/delixon-labs/qiloback-worker:0.3.3
```

Three images cover the control plane (platform-api), the generated
runtime (runtime-api), and the background worker (Celery). A reference
`docker-compose.yml` covering Postgres, Redis, Caddy and the three
images lands in `docs/self-host.md` (in progress).

### Self-host: Helm chart

```bash
helm repo add qiloback https://delixon-labs.github.io/qiloback-helm
helm install qiloback qiloback/qiloback --version 0.3.3
```

For Kubernetes deployments. The chart provisions the same three
services plus an `ingress`, `Postgres` (subchart), `Redis` (subchart),
and the secrets/configmaps the apps need.

### Coming next ⏳

- **Homebrew tap:** `brew install delixon-labs/tap/qiloback`
- **Scoop bucket:** `scoop bucket add delixon-labs https://github.com/delixon-labs/scoop-bucket && scoop install qiloback`
- **WinGet:** `winget install delixon.qiloback`
- **AUR:** `yay -S qiloback`

These pick up automatically once the corresponding GitHub release ships
its `qiloback-darwin-x64` asset (currently waiting on the GitHub-hosted
macOS-x64 runner queue).

## What you can do with the CLI

Once installed, `qiloback --help` lists every command. The 26 commands
group into nine functional buckets:

### Bootstrap

| Command | What it does |
|---|---|
| `qiloback init [path] -t <template>` | Scaffold a new project from a template |
| `qiloback templates list` | List the bundled templates |
| `qiloback templates apply <name>` | Apply a template in-place to an existing project |

Bundled templates: `saas-starter`, `ecommerce`, `cms`, `crm`,
`marketplace`, `helpdesk`, `inventory`, `lms`, `project-management`,
`real-estate`, `social-network`.

### DSL (the YAML manifest)

| Command | What it does |
|---|---|
| `qiloback validate qiloback.yml` | Schema + semantic check |
| `qiloback generate` | Generate FastAPI sources, SQLAlchemy models, Alembic migrations, pytest tests, OpenAPI spec, and SDKs from the DSL |
| `qiloback status` | Active project state — DSL, components, last generation |
| `qiloback doctor` | Verify Python, Docker, Postgres client, Node toolchain |

### Local development

| Command | What it does |
|---|---|
| `qiloback dev up/down/logs` | Manage the docker-compose stack — Postgres, Redis, the runtime API |
| `qiloback seed file.sql` | Seed the database with initial data |
| `qiloback migrate up/down/current` | Alembic migration management |
| `qiloback types ts` / `qiloback types py` | Generate TypeScript or Python types from the live database schema |

### AI assistance

| Command | What it does |
|---|---|
| `qiloback ai generate "<prompt>"` | "Add a billing entity with monthly subscriptions" → DSL diff |
| `qiloback ai review` | Static review of the current DSL — flags unused indexes, RLS gaps, naming inconsistencies |
| `qiloback ingest <frontend-dir>` | Walk a Next.js/React tree and synthesise a backend DSL from the inferred entities |

### APIs and SDKs

| Command | What it does |
|---|---|
| `qiloback openapi export` | Generate the OpenAPI 3.1 specification for the runtime |
| `qiloback sdk gen ts/py/dart` | Generate typed SDK clients from the DSL |

### Marketplace

| Command | What it does |
|---|---|
| `qiloback components browse` | Browse the component marketplace |
| `qiloback components install <name>` | Add a component to the current project |
| `qiloback components inspect <name>` | Show a component's manifest, contracts, and example usage |
| `qiloback plugin list/install` | Third-party plugins |

### Realtime / CDC

| Command | What it does |
|---|---|
| `qiloback realtime status` | Inspect the Postgres logical-replication CDC listener |
| `qiloback dbwebhook list/test` | Manage row-level Postgres webhooks |
| `qiloback passkey list` | List registered WebAuthn passkeys (registration itself happens in the browser) |

### Edge functions

| Command | What it does |
|---|---|
| `qiloback function deploy <name>` | Deploy an edge function |
| `qiloback function list` | List deployed functions |

### Eject and deploy

| Command | What it does |
|---|---|
| `qiloback project eject` | Hand off the generated FastAPI source under Apache 2.0 — the QiloBack license stays on the generator, never on the code it writes for you |
| `qiloback deploy` | Sync the project to the configured self-host target and restart the container stack |
| `qiloback benchmark` | Performance regression suite against a running runtime API |
| `qiloback mcp serve` | Run the MCP server locally for AI-tool integration |

## Typical first-time flow

```bash
# 1. Install
npm install -g @qiloback/qiloback     # or: pip install qiloback-cli

# 2. Verify environment
qiloback doctor

# 3. Scaffold from a template
qiloback init my-saas --template saas-starter
cd my-saas

# 4. Edit qiloback.yml — install the VS Code extension for inline
# autocomplete and validation against the live JSON schema.

# 5. Validate
qiloback validate qiloback.yml

# 6. Generate the FastAPI backend
qiloback generate

# 7. Spin up Postgres + Redis + the API locally
qiloback dev up

# 8. Hit it from Python
pip install qiloback-sdk
python -c "from qiloback import Client; c = Client('http://localhost:8001'); print(c.projects.list())"

# 9. When you decide to leave QiloBack, take the source with you
qiloback project eject     # writes a clean Apache-2.0 FastAPI tree
```

## Where to go next

- [README](../README.md) — project overview and the licensing posture (FSL → Apache 2.0)
- [CHANGELOG](../CHANGELOG.md) — version history
- [SECURITY](../SECURITY.md) — how to report a vulnerability responsibly
- [CONTRIBUTING](../CONTRIBUTING.md) — pull-request flow and contributor guidelines
- [LICENSE](../LICENSE) and [LICENSE-FAQ](../LICENSE-FAQ.md) — full license text and clarifications

Detailed guides — DSL reference, module catalogue, RLS recipes,
deployment runbooks — land here on the same cadence as each tagged
release converts from FSL to Apache 2.0.
