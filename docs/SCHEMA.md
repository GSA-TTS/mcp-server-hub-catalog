# Catalog Entry Schema

This document describes the schema for MCP server catalog entries in this
repository. Each server is defined by a single YAML file at the repository root
(one file per server). The format follows the
[obot-platform/mcp-catalog](https://github.com/obot-platform/mcp-catalog)
entry format so that entries render correctly in the obot MCP gateway UI.

## File conventions

- **One file per server**, named in `snake_case` matching the entry `name`
  (e.g. `nih_reporter.yaml` → `name: nih_reporter`).
- Files live at the repository **root** — there is no category nesting.
- Files are plain YAML (no Markdown frontmatter).

## Fields

### Required fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable display name for the server (e.g. `NIH RePORTER`). Also used as the filename stem in `snake_case`. |
| `entryKey` | string | Globally unique key for the entry, prefixed with `obot-` (e.g. `obot-reporter`). Used by the gateway to identify the entry. |
| `serverUserType` | enum | Whether users share one instance or each get their own. Use `multiUser` for servers that need no per-user credentials (e.g. those querying a public, keyless API) — all users share a single gateway-hosted instance. Use `singleUser` only when each user must supply their own upstream credentials, so each gets an isolated instance. |
| `shortDescription` | string | One-line summary shown in catalog list views. |
| `repoURL` | string (URL) | Link users can follow for more information. For obot's own entries this points to the server's documentation; for GSA-hosted remote servers it may point to the running `/mcp` endpoint or the source repository. |
| `runtime` | enum | How the server runs. Use `remote` for an externally hosted HTTP/SSE endpoint, or `containerized` for a server the gateway itself hosts as a Docker container. |
| `remoteConfig` | object | Connection configuration for `remote` servers. Required when `runtime: remote`. See below. |
| `containerizedConfig` | object | Runtime configuration for `containerized` servers. Required when `runtime: containerized`. See below. |

### `remoteConfig` (required when `runtime: remote`)

A `remote` server runs somewhere outside the gateway (e.g. on cloud.gov) and is
reachable at a fixed public URL. The gateway proxies to that URL. **Because the
URL is public, a `remote` server is reachable independently of the gateway.**

| Field | Type | Description |
|-------|------|-------------|
| `fixedURL` | string (URL) | The fixed MCP endpoint the gateway connects to (e.g. `https://<app>.app.cloud.gov/mcp`). |

### `containerizedConfig` (required when `runtime: containerized`)

A `containerized` server is hosted **by the gateway itself**: the gateway pulls
the image and runs it as a container, then proxies client requests to it. The
container has **no public route** — it is reachable only through the gateway,
which is what makes it suitable for gateway-only access, usage monitoring, and
access control.

> **Image pull:** with the gateway's Docker runtime backend, images are pulled
> without registry authentication. The image **must be publicly pullable**
> (e.g. a public GHCR or Docker Hub image). Private registries (including ECR)
> require the Kubernetes backend and are not supported by the current pilot
> deployment.

| Field | Type | Description |
|-------|------|-------------|
| `image` | string | **Required.** Fully-qualified, publicly pullable image reference, ideally pinned (e.g. `ghcr.io/gsa-tts/mcp-server-nih-reporter:0.2.0`). |
| `port` | integer | **Required.** Port the server listens on inside the container (e.g. `8080`). |
| `path` | string | **Required.** HTTP path of the MCP (streamable HTTP) endpoint (e.g. `/mcp`). |
| `healthzPath` | string | Optional. HTTP path for a readiness/health check (e.g. `/health`). If omitted, the gateway probes the MCP endpoint. |
| `command` | string | Optional. Override the container's default command. |
| `args` | list | Optional. Arguments passed to the command. |
| `startupTimeoutSeconds` | integer | Optional. Seconds to wait for the server to become ready (default 60, max 600). |

> **Per-user / shared configuration (API keys, etc.) does NOT go here.** It is a
> **top-level `env` list** on the entry — a sibling of `runtime` and
> `containerizedConfig`, not nested inside `containerizedConfig`. See
> [`env` (user/shared configuration)](#env-usershared-configuration) below.

### `env` (user/shared configuration)

Declares environment variables the server needs — most importantly the fields
Obot **prompts the user for** and injects into the deployed container. This is
how a `singleUser` server collects a per-user API key.

**This is a top-level field on the entry** (a sibling of `runtime` /
`containerizedConfig` / `remoteConfig`), matching the upstream obot catalog
(e.g. `firecrawl.yaml`). Do **not** nest it under `containerizedConfig`:

> **Gotcha (learned the hard way):** if `env` is nested under
> `containerizedConfig`, Obot does **not** parse it as user configuration. The
> UI then shows only the connection URL with **no field to enter the key**, the
> container launches **without** the variable set, and tool calls fail (e.g.
> `EIA_API_KEY is not set`). Placing `env` at the top level fixes this.

Each item has the same shape as the upstream obot catalog:

| Field | Type | Description |
|-------|------|-------------|
| `key` | string | **Required.** The environment variable name passed to the server (e.g. `EIA_API_KEY`). |
| `name` | string | Human-friendly label shown in the Obot config UI (e.g. `EIA API Key`). |
| `description` | string | Help text shown under the field (e.g. where to get the key). |
| `required` | boolean | Whether the user must supply a value before the server can be enabled. |
| `sensitive` | boolean | Whether the value is a secret — masked in the UI and stored securely. Use `true` for API keys/tokens. |

For a `singleUser` server, each user is prompted for these values and gets them
injected into their own isolated instance. For a shared `multiUser` server, the
values are configured once and shared by all users.

Example (top-level, alongside `runtime` / `containerizedConfig`):

```yaml
env:
  - key: EIA_API_KEY
    name: EIA API Key
    description: Your personal EIA Open Data API key (free at https://www.eia.gov/opendata/register.php)
    required: true
    sensitive: true
runtime: containerized
containerizedConfig:
  image: ghcr.io/gsa-tts/mcp-server-eia:0.1.0
  port: 8080
  path: /mcp
  healthzPath: /health
```

> Omit `env` entirely if the server needs no configuration (e.g. the keyless,
> public-API `multiUser` servers in this catalog).

### Optional fields (recommended for a rich catalog listing)

These fields are not required for the entry to function but produce a much
richer listing in the gateway UI. See `asana.yaml` in the upstream obot catalog
for a complete example.

| Field | Type | Description |
|-------|------|-------------|
| `description` | string (multi-line Markdown) | Long-form description rendered on the server's detail page. Supports Markdown headings, lists, and emphasis. Conventionally includes **Features**, **What you'll need to connect**, and **Examples** sections. Use the YAML block scalar `\|` so Markdown is preserved. |
| `metadata` | object | Display metadata for filtering and grouping (see below). |
| `metadata.categories` | string | Comma-separated category labels (e.g. `Health, Research`). |
| `metadata.allow-multiple` | string (`"true"`/`"false"`) | Whether multiple instances of this server may be configured. |
| `icon` | string (URL) | URL to an icon image displayed next to the entry. |
| `toolPreview` | list | A preview of the tools the server exposes. Each item documents one tool (see below). |

### `toolPreview` items

Each entry in `toolPreview` describes a single MCP tool:

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | The tool's registered name (e.g. `find_project_ids`). |
| `description` | string | One-line explanation of what the tool does and when to use it. |
| `params` | object | Map of `param_name: "description"` for the tool's parameters. |

## Minimal example

```yaml
name: nih_reporter
entryKey: obot-reporter
serverUserType: multiUser
shortDescription: Access data from the NIH RePORTER API
repoURL: https://nih-reporter-mcp-server.app.cloud.gov/mcp
runtime: remote
remoteConfig:
  fixedURL: https://nih-reporter-mcp-server.app.cloud.gov/mcp
```

## Minimal containerized (gateway-hosted) example

The gateway pulls the image and runs it; the server is reachable only through
the gateway (no public route). The image must be publicly pullable.

```yaml
name: nih_reporter
entryKey: obot-reporter
serverUserType: multiUser
shortDescription: Access data from the NIH RePORTER API
repoURL: https://github.com/GSA-TTS/mcp-server-nih-reporter
runtime: containerized
containerizedConfig:
  image: ghcr.io/gsa-tts/mcp-server-nih-reporter:0.2.0
  port: 8080
  path: /mcp
  healthzPath: /health
```

> **`serverUserType` for public-data servers:** the servers in this catalog
> query public, keyless APIs and need no per-user credentials, so they use
> `multiUser` — all users share one gateway-hosted instance. `multiUser`
> containerized entries are deployed once (by an admin/power user) and shared;
> `singleUser` would instead spin up a separate container per user, which only
> makes sense when each user supplies their own upstream credentials.

## Per-user containerized example (`singleUser` + top-level `env`)

When each user must supply their own credential (e.g. a personal API key), use
`serverUserType: singleUser` and declare the credential as a **top-level `env`**
field (a sibling of `runtime` / `containerizedConfig` — **not** nested inside
`containerizedConfig`). Obot renders these fields in its config UI, prompts each
user, and injects the values into that user's own container instance.

```yaml
name: EIA Open Data
entryKey: obot-eia
serverUserType: singleUser
shortDescription: Query U.S. Energy Information Administration (EIA) Open Data API v2
repoURL: https://github.com/GSA-TTS/mcp-server-eia
env:                              # <-- TOP LEVEL, not under containerizedConfig
  - key: EIA_API_KEY
    name: EIA API Key
    description: Your personal EIA Open Data API key (free at https://www.eia.gov/opendata/register.php)
    required: true
    sensitive: true
runtime: containerized
containerizedConfig:
  image: ghcr.io/gsa-tts/mcp-server-eia:0.1.0
  port: 8080
  path: /mcp
  healthzPath: /health
```

> If `env` is nested under `containerizedConfig`, Obot will not treat it as user
> configuration: the UI shows only the connection URL (no key field), the
> container launches without the variable, and tool calls fail (e.g.
> `EIA_API_KEY is not set`). See the [`env`](#env-usershared-configuration)
> field reference above.

## Enriched example

```yaml
name: NIH RePORTER
entryKey: obot-reporter
serverUserType: multiUser
shortDescription: Search and analyze NIH grant funding data from the RePORTER API
description: |
  A Model Context Protocol (MCP) server for the NIH RePORTER grant database.

  ## Features
  - **Search NIH-funded projects** by topic, PI, organization, year, and more
  - **Summarize funding portfolios** with exact or sampled statistics
  - **Rank top-funded PIs and institutions**
  - **Generate interactive dashboards and tables**

  ## What you'll need to connect
  No setup required — the server queries the public NIH RePORTER API.

  ## Examples
  - "Who are the top-funded PIs in cancer research?"
  - "Total NIH funding for aging grants in FY2023"
metadata:
  categories: Health, Research, Government
  allow-multiple: "false"
icon: https://api.reporter.nih.gov/favicon.ico
repoURL: https://github.com/GSA-TTS/mcp-server-nih-reporter
runtime: remote
remoteConfig:
  fixedURL: https://nih-reporter-mcp-server.app.cloud.gov/mcp
toolPreview:
  - name: find_project_ids
    description: Primary search tool. Returns a page of matching project IDs plus overview statistics.
    params:
      search_params: "Search criteria (term, years, agencies, organizations, PI, spending categories)"
      offset: "Zero-based result offset for pagination"
      limit: "Number of project IDs to return (max 500)"
```

## Validation

Before committing a new or changed entry, verify it is well-formed YAML and
contains the required fields. See [`CONTRIBUTING.md`](../CONTRIBUTING.md) for the
full checklist.
