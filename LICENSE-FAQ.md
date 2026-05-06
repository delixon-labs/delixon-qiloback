# QiloBack — License FAQ

QiloBack is **source-available** software under the
[Functional Source License (FSL-1.1-ALv2)](LICENSE).

This is not open source in the traditional sense. The installation
wrappers, user documentation and compiled binaries are publicly
available. The core source code is visible to invited contributors
during the FSL window and becomes public two years after each
release. One usage restriction applies: you cannot use the code to
build a competing commercial product.

---

## What you CAN do

- Use QiloBack internally at your company, regardless of size
- Read, study and learn from each release's source code (public two
  years after release; available earlier under NDA for enterprise
  audits)
- Modify the code for your personal or internal use
- Use it for non-commercial education and research
- Provide professional services to others who use QiloBack
- Self-host the platform on your own infrastructure
- Export and run the generated FastAPI backends anywhere — those are
  yours to keep, no QiloBack license attaches to the generated output
- Contribute improvements back to the project

## What you CANNOT do

- Sell or offer a commercial product or service that competes with
  QiloBack
- Offer the same or substantially similar functionality as a
  commercial service
- Repackage or rebrand it as your own product

---

## Common questions

**Can I use it at my company internally?**
Yes. Internal use is explicitly permitted, regardless of company size.

**Can a consultant customize QiloBack for a client?**
Yes, as long as the client uses it internally and the consultant is
not selling a competing product.

**Does a private fork for internal use count as competing?**
No. Internal use is always permitted.

**Can I build a SaaS that does the same thing as QiloBack?**
No. That would be a Competing Use under the license terms.

**The backends QiloBack generates — what license do those carry?**
The output is yours. QiloBack's license covers the generator and the
control plane, not the FastAPI code you generate from your DSL.
Generated backends are unencumbered — you can ship them under any
license you choose, including a closed proprietary license.

**When does QiloBack itself become Apache 2.0?**
Two years after each version's release date. After that date, you may
use that version under the full terms of the Apache License 2.0,
including commercial use. Example: QiloBack `v1.0.0` released on
`2026-09-15` becomes Apache 2.0 on `2028-09-15` — automatically,
without any action from us.

**Is QiloBack open source?**
No, not during the first two years of each release. QiloBack is
*source-available*: during the FSL window the core source is
accessible to invited contributors (CLA) and available for formal
code audits under NDA. Two years after each release, that version
converts to Apache 2.0 automatically and the source becomes public.

**Why not Apache 2.0 from day one?**
Building QiloBack takes resources. FSL lets us share the code with
the community while protecting the project during its growth phase.
After two years, every version becomes open source regardless of
what we do — it's a commitment coded into the license, not a promise.

**Can I audit the code before using QiloBack in a regulated industry?**
Yes. For enterprise compliance requirements (SOC2, HIPAA, ISO 27001,
PCI), we offer formal code audits under NDA. Each version's source
also becomes publicly auditable two years after release when it
converts to Apache 2.0. Contact: `legal@delixon.dev`.

**Where is the source code?**
During the FSL window the core source lives in a private repository
accessible to invited contributors and to enterprise customers under
NDA. The installation wrappers and documentation live in a public
repository. Two years after each release, that version's full source
becomes publicly browseable under Apache 2.0.

**How do I know QiloBack isn't sending my data somewhere?**
QiloBack is honest about telemetry. The self-hosted control plane has
no required cloud component. The hosted SaaS at `qiloback.dev`
processes only what an account holder explicitly sends. There is no
silent telemetry baked into the generated backends — those run on
your infrastructure under your control.

**What happens if Delixon Labs disappears?**
Three things protect you:

1. **The generated backends are yours.** They are FastAPI codebases
   with no runtime dependency on QiloBack. They keep running.
2. **The binary you have already downloaded keeps working.**
3. **Every version converts to Apache 2.0 after two years** — `v1.0.0`
   becomes fully open source in 2028 regardless of what happens to
   us. The conversion is coded in the license, not promised.

**Can I contribute?**
Yes. For bug fixes, feature suggestions and small improvements, PRs
and issues are welcome in the public wrapper repository. For larger
contributions touching the core, we may require a Contributor License
Agreement (CLA). See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Legal entity

| Role | Entity |
|------|--------|
| Copyright holder and licensor | XPlus Technologies LLC |
| Public brand | Delixon Labs |
| Product | QiloBack |

Delixon Labs is the developer tools division of
[XPlus Technologies LLC](https://xplustechnologies.com).

For licensing inquiries: `legal@delixon.dev`.
