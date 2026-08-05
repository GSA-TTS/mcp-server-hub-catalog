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
| `serverUserType` | enum | Who the server authenticates as. Use `singleUser` for servers scoped to an individual user. |
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
| `env` | list | Optional. Environment variables the server needs. Same item shape as documented by the upstream obot catalog (`key`, `name`, `required`, `sensitive`, `description`). Omit entirely if the server needs none. |

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
serverUserType: singleUser
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
serverUserType: singleUser
shortDescription: Access data from the NIH RePORTER API
repoURL: https://github.com/GSA-TTS/mcp-server-nih-reporter
runtime: containerized
containerizedConfig:
  image: ghcr.io/gsa-tts/mcp-server-nih-reporter:0.2.0
  port: 8080
  path: /mcp
  healthzPath: /health
```

## Enriched example

```yaml
name: NIH RePORTER
entryKey: obot-reporter
serverUserType: singleUser
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
