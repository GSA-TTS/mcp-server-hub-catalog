# AGENTS.md — MCP Server Hub Catalog

Instructions for an AI agent adding or updating a server entry in this
catalog. This is the **project-level** contract; it is additive to any
universal agent rules and never overrides them.

> **What this repo is:** the catalog of MCP servers the GSA-managed **obot MCP
> gateway** connects to. Each server is one YAML file at the repo root. The
> gateway reads these files to populate its UI and learn how to connect.
>
> **Scope of this file:** the *catalog* side only — writing, validating, and
> landing a catalog entry. Containerizing the upstream server (Dockerfile →
> public GHCR image) happens in the **server's own repo**; see
> [Reference examples](#reference-examples).

---

## Canonical references (read before editing)

| Doc | Purpose |
|-----|---------|
| [`docs/SCHEMA.md`](docs/SCHEMA.md) | Full field reference for a catalog entry. **Source of truth for fields.** |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Human workflow + validation checklist. |
| [`README.md`](README.md) | Server table + repo structure (must be updated per new server). |

If this file and `docs/SCHEMA.md` ever disagree on a field, **`docs/SCHEMA.md`
wins** — fix this file to match.

## File conventions

- **One file per server** at the repo **root**, named in `snake_case`
  (e.g. `nci_evs.yaml`). No category nesting.
- Plain YAML, no Markdown frontmatter, no tabs.
- `entryKey` MUST be globally unique and prefixed with `obot-`.
- Never commit secrets/credentials. Entries describe **how to connect**, not
  how to authenticate with private credentials.

---

## Runbook — add a `containerized` server

This is the pattern used for the servers currently in the catalog (they wrap
public, keyless federal-data APIs and are hosted by the gateway as containers).
The **NCI EVS** entry is the worked example throughout.

### Prerequisite (in the server's own repo, not here)

A **publicly pullable, version-pinned** image must already exist and serve MCP
over streamable HTTP. Confirm before writing the entry:

```bash
docker manifest inspect ghcr.io/gsa-tts/mcp-server-<name>:<version>   # must succeed (public)
```

Do **not** author a catalog entry that pins an image which is not yet public and
pullable — the gateway's Docker runtime pulls without auth, so a private image
(including ECR) will fail. See [Reference examples](#reference-examples) for how
that image is built.

### Step 1 — Create `<name>.yaml` at the repo root

Required fields (see `docs/SCHEMA.md` for the authoritative list):

```yaml
name: NCI EVS                 # display name; filename stem is snake_case of this
entryKey: obot-nci-evs        # UNIQUE across the catalog, prefixed obot-
serverUserType: multiUser     # see decision below
shortDescription: Search and navigate NCI cancer terminology (NCIt / NCIm) via the EVS API
repoURL: https://github.com/GSA-TTS/mcp-server-nci-evs
runtime: containerized
containerizedConfig:
  image: ghcr.io/gsa-tts/mcp-server-nci-evs:0.2.0   # public + version-pinned
  port: 8080          # MUST match what the container serves
  path: /mcp          # MUST match the MCP endpoint path
  healthzPath: /health
```

Then enrich (strongly recommended) with `description` (Markdown block scalar
with **Features / What you'll need to connect / Examples**), `metadata`
(`categories`, `allow-multiple`), `icon`, and `toolPreview`. Copy the shape from
an existing entry such as [`nci_evs.yaml`](nci_evs.yaml).

**`serverUserType` decision (get this right — it was a real correction):**

- Use **`multiUser`** when the server needs **no per-user credentials** (e.g. it
  queries a public, keyless API). All users share one gateway-hosted instance.
  **Every current server in this catalog is `multiUser`** — match that default.
- Use **`singleUser`** only when each user must supply their **own upstream
  credentials**, so each gets an isolated instance.

`runtime: remote` is also valid (externally hosted at a fixed public URL via
`remoteConfig.fixedURL`) — see `docs/SCHEMA.md`. The catalog currently uses
`containerized`.

### Step 2 — Add a docs page

Create `docs/servers/<name>.md` (overview, data source, runtime, tools table).
Use [`docs/servers/nci_evs.md`](docs/servers/nci_evs.md) as the template.

### Step 3 — Add an icon

Add `icons/<name>.png` and reference it from the entry as the raw GitHub URL:
`https://raw.githubusercontent.com/GSA-TTS/mcp-server-hub-catalog/main/icons/<name>.png`.
Match the size of existing icons (128×128 is typical).

### Step 4 — Update the README

Add a row to the server table **and** the repo-structure tree in
[`README.md`](README.md).

---

## Verification (MUST pass before opening a PR)

Run the full checklist in [`CONTRIBUTING.md`](CONTRIBUTING.md#validation-checklist).
At minimum:

```bash
# 1. Valid YAML + required fields + expected serverUserType
python -c "import yaml; d=yaml.safe_load(open('<name>.yaml')); \
  assert {'name','entryKey','serverUserType','shortDescription','repoURL','runtime'} <= d.keys(); \
  print('ok', d['entryKey'], d['serverUserType'])"
# (no PyYAML on the host? use: uv run --with pyyaml python -c "...")

# 2. entryKey is unique across the catalog (expect exactly ONE match)
grep -h '^entryKey:' *.yaml | sort | uniq -d   # prints nothing if all unique

# 3. Image is public + pullable, and port/path match the container
docker manifest inspect <containerizedConfig.image>
```

Confirm also: `docs/servers/<name>.md` exists; README table + tree updated; icon
present; no secrets.

> Prefer the dedicated tools (Read/Grep/Glob/Edit) over ad-hoc shell for file
> work; the shell snippets above are the verification gates, not editing steps.

## Landing the change (PR discipline)

- **One server per PR** (established convention — see git history).
- Branch from an **up-to-date `main`** (`git checkout main && git pull --ff-only`).
  This catalog moves fast; a stale base is how NCI EVS shipped as `singleUser`
  and needed a follow-up `*-multiuser` PR.
- Commit message: `feat: add <Server Name> to catalog` (or
  `feat: <server> <change>` for updates).
- PR description SHOULD include: context, the changed files, the verification
  output (YAML valid, entryKey unique, image public), rollback (revert the PR),
  and security impact (usually "none — public API, no credentials").
- Do not self-merge; wait for human review.

## After merge

- Re-sync the catalog source in the **obot admin UI** so the gateway indexes the
  new entry, then deploy the server. See the server-hub deployment notes in the
  `mcp-server-hub` repo.

---

## Reference examples

Real servers built and cataloged with this pattern. Use them as concrete
templates, including how the **upstream image** is produced in the server's own
repo:

- **NCI EVS** — [entry](nci_evs.yaml) · [docs](docs/servers/nci_evs.md) ·
  server repo [`GSA-TTS/mcp-server-nci-evs`](https://github.com/GSA-TTS/mcp-server-nci-evs)
  (see its `Dockerfile` and `scripts/build-and-push.sh` for the
  Dockerfile → public GHCR image flow).
- **NIH RePORTER** — [entry](nih_reporter.yaml) · [docs](docs/servers/nih_reporter.md) ·
  server repo [`GSA-TTS/mcp-server-nih-reporter`](https://github.com/GSA-TTS/mcp-server-nih-reporter)
  (the original containerized pattern).
