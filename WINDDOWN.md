# Wind-Down Notes — MCP Server Hub Catalog

> **Status:** The GSA-TTS MCP Server Hub effort is being **wound down.** This
> file records the state of the catalog for a future team. It is a snapshot for
> developers, not GSA policy.
>
> **This repo is one of four.** See the cross-repo map in the
> [`GSA-TTS/mcp-server-hub`](https://github.com/GSA-TTS/mcp-server-hub) repo
> (`planning/WINDDOWN-INDEX.md`) for how `mcp-server-hub`, the `obot` fork, this
> catalog, and `mcp-server-hub-tools` fit together.

---

## 1. What this repo is

The **catalog** of MCP (Model Context Protocol) servers exposed through the
GSA-managed **Obot MCP gateway**. The gateway indexes this Git repo to populate
its catalog UI and learn how to connect to each server. Entry format follows the
upstream [`obot-platform/mcp-catalog`](https://github.com/obot-platform/mcp-catalog)
convention.

All cataloged servers are **pilots / proofs-of-concept** wrapping **public
federal-data APIs** — consistent with the hub's open-data-only guardrail (see the
`mcp-server-hub` ROADMAP). They are not production services.

## 2. Repo health at wind-down

**This is the healthiest of the four repos.** `main` is clean, up to date with
`origin/main`, no uncommitted changes, no `TODO`/`FIXME`/`WIP` markers, and every
entry has complete required fields, a unique `entryKey`, an icon, and a docs
page. Latest substantive work was the NEPA suite through late August 2026.

Unlike the `obot` and `mcp-server-hub-tools` forks, there is **no uncommitted
work to preserve here** — everything of value is already on `main`.

## 3. What's in the catalog (29 entries)

29 catalog entries, all `runtime: containerized`, 25 `multiUser` (shared,
keyless) and 4 `singleUser` (per-user API key: `eia.yaml`, `regulations_gov.yaml`,
`census.yaml`, `epa_aqs.yaml`).

**Group A — standalone data-API servers (11):** `nih_reporter`,
`nih_clinicaltrials`, `cdc_places`, `ncbi_eutils`, `nci_evs` (health/research);
`eia`, `grants_gov`, `regulations_gov`; `fema_nfhl`, `usgs_nhdplus_hr`,
`blm_mlrs`, `usace_iwr`.

**Group B — NEPA environmental-screening suite (17):** `blm`, `cfr`, `census`,
`efh`, `epa_aqs`, `epa_acres`, `esa_ranges`, `nepa_fema_nfhl`, `gbif`, `ipac`,
`noaa`, `nrhp`, `padus`, `pcsrf`, `usace`, `tribal`, `tigerweb_counties`. Most
share the monorepo `GSA-TTS/nepa-mcp`.

> `fema_nfhl.yaml` and `nepa_fema_nfhl.yaml` are two distinct entries wrapping
> the same FEMA service (standalone vs. NEPA-suite versions).

Per-server documentation lives in [`docs/servers/`](docs/servers/) (one Markdown
page per entry); `docs/servers/nih_reporter.md` is the template.

## 4. How the catalog works (for whoever resumes it)

- **One YAML file per server at the repo root**, `snake_case` filename.
- Schema is authoritatively defined in [`docs/SCHEMA.md`](docs/SCHEMA.md) (wins
  over `AGENTS.md` on any conflict). Key fields: `name`, `entryKey` (globally
  unique, `obot-` prefixed), `serverUserType`, `shortDescription`, `repoURL`,
  `runtime`, and one of `remoteConfig` / `containerizedConfig`. Optional:
  `description`, `metadata`, `icon`, `toolPreview`, and a top-level `config` list.
- **Gotcha:** per-user environment values use top-level `config` entries with
  `usage: env`,
  NOT nested under `containerizedConfig` — nesting it breaks the config-field UI
  (documented in `AGENTS.md` and the hub's `obot/README.md`).
- **Containerized images must be publicly pullable and version-pinned** — the
  gateway's Docker backend has no registry auth (no ECR/private). Images must be
  **linux/amd64** to match the gateway host.
- **After merging a catalog change**, re-sync the catalog source in the Obot
  admin UI and re-deploy the server; config changes require a fresh deploy.
- Contribution discipline (from `CONTRIBUTING.md` / `AGENTS.md`): one server per
  PR, branch from fresh `main`, no self-merge. `scripts/make_icon.py` normalizes
  icons to 128×128 transparent-padded PNGs.

## 5. Lingering branches (housekeeping)

`main` is complete, but several old feature/fix branch refs still exist locally
and on `origin`. Branches **not merged into `origin/main`** at wind-down:

- `origin/add-USACE-IWR-server`
- `origin/feat/add-eia-catalog-entry`
- `origin/feat/cdc-places-containerized`
- `origin/feat/ncbi-eutils-containerized`
- `origin/feat/nih-clinicaltrials-containerized`
- `origin/feat/nih-reporter-containerized`

**These appear to be superseded, not lost work.** Spot-checks show their content
(the corresponding servers) already present on `main` via later PRs — the diffs
against `main` are dominated by *deletions* of entries `main` has that the old
branch predates. They are stale, not ahead. Safe to delete after a final human
confirmation; no action taken here.

- `add-login.gov-logo`: the `icons/login_gov.png` it added is **already on
  `main`** — this branch is fully merged/superseded. The logo is for the
  login.gov auth provider in `mcp-server-hub-tools`; no catalog *entry* uses it
  (login.gov is an auth provider, not an MCP server).

## 6. If you resume

1. `main` is the source of truth; start from a fresh clone.
2. Follow `CONTRIBUTING.md` + `docs/SCHEMA.md` to add/modify entries.
3. Prune the stale branches in §5 after confirming their servers are on `main`.
4. Remember catalog changes are inert until re-synced + re-deployed in the Obot
   gateway (see the hub repo's `obot/README.md`).

## 7. Provenance

- **Remote:** `https://github.com/GSA-TTS/mcp-server-hub-catalog.git`
- Point of contact: _(fill in team/POC before archiving)_
- This wind-down documentation was AI-assisted and requires human review.
