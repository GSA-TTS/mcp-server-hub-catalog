# Contributing to the MCP Server Hub Catalog

This catalog lists the MCP (Model Context Protocol) servers available through
the GSA-managed obot MCP gateway. This guide explains how to add a new server or
update an existing one.

## Overview

Each MCP server is described by a single YAML file at the repository root. The
gateway reads these files to populate the catalog UI and to know how to connect
to each server. The entry format follows the
[obot-platform/mcp-catalog](https://github.com/obot-platform/mcp-catalog)
convention.

Before contributing, review [`docs/SCHEMA.md`](docs/SCHEMA.md) for the full field
reference.

## Adding a new server

A server can be added in one of two runtimes:

- **`remote`** — the server runs somewhere outside the gateway (e.g. cloud.gov)
  at a fixed public URL, and the gateway proxies to it. The URL is public, so
  the server is reachable independently of the gateway.
- **`containerized`** — the gateway hosts the server itself as a Docker
  container from a published image. The container has **no public route** and is
  reachable only through the gateway, which is the preferred model for
  gateway-only access, usage monitoring, and access control.

### Option A — remote server

1. **Confirm the server is deployed and reachable.** The gateway connects to a
   fixed remote endpoint (typically a cloud.gov `/mcp` URL). Verify the endpoint
   responds before adding it to the catalog.

2. **Create the entry file.** Add a new file named `<name>.yaml` in
   `snake_case` at the repository root. At minimum it must contain the required
   fields:

   ```yaml
   name: my_server
   entryKey: obot-my-server
   serverUserType: multiUser
   shortDescription: Access data from the Example API
   repoURL: https://github.com/GSA-TTS/mcp-server-my-server
   runtime: remote
   remoteConfig:
     fixedURL: https://my-server-mcp-server.app.cloud.gov/mcp
   ```

### Option B — containerized (gateway-hosted) server

1. **Publish a public image.** Build a container that serves MCP over
   streamable HTTP on a known port and path (conventionally `:8080/mcp`) and
   exposes a health path (conventionally `/health`). Push it to a **publicly
   pullable** registry (public GHCR or Docker Hub) — the gateway's Docker
   runtime backend pulls without registry authentication, so private images
   (including ECR) are not supported by the current pilot deployment. Pin the
   image to a version tag.

2. **Verify the image runs.** Confirm the container answers on its health and
   MCP endpoints, e.g.:

   ```bash
   docker run --rm -p 8080:8080 <image>
   curl -s localhost:8080/health   # expect {"status":"healthy",...}
   ```

3. **Create the entry file** at the repository root:

   ```yaml
   name: my_server
   entryKey: obot-my-server
   serverUserType: multiUser
   shortDescription: Access data from the Example API
   repoURL: https://github.com/GSA-TTS/mcp-server-my-server
   runtime: containerized
   containerizedConfig:
     image: ghcr.io/gsa-tts/mcp-server-my-server:1.0.0
     port: 8080
     path: /mcp
     healthzPath: /health
   ```

### Both options

3. **Enrich the entry (recommended).** Add `description`, `metadata`, `icon`,
   and `toolPreview` fields so the entry renders richly in the gateway. See the
   [enriched example](docs/SCHEMA.md#enriched-example) in the schema doc.

4. **Add a server documentation page.** Create
   `docs/servers/<name>.md` describing the server, its data source, and the
   tools it exposes. Use an existing page such as
   [`docs/servers/nih_reporter.md`](docs/servers/nih_reporter.md) as a template.

5. **Update the README.** Add a row to the server table in
   [`README.md`](README.md) linking to the new documentation page.

## Field conventions

- `entryKey` MUST be globally unique and prefixed with `obot-`.
- `name` and the filename stem SHOULD match (in `snake_case`).
- For remote servers, `remoteConfig.fixedURL` is the endpoint the gateway
  connects to. It is often — but not required to be — identical to `repoURL`.
- For containerized servers, `containerizedConfig.image` MUST be a publicly
  pullable, version-pinned image reference; `port` and `path` MUST match what
  the container actually serves.
- Use `serverUserType: multiUser` for servers that need no per-user
  credentials (e.g. those querying a public, keyless API) — all users share one
  gateway-hosted instance. Use `singleUser` only when each user must supply
  their own upstream credentials.
- Never commit secrets, API keys, or credentials in a catalog entry. Catalog
  entries describe **how to connect**, not **how to authenticate with private
  credentials**.

## Validation checklist

Before opening a pull request, confirm:

- [ ] The file is valid YAML (no tabs, correct indentation).
- [ ] All required common fields are present (`name`, `entryKey`,
      `serverUserType`, `shortDescription`, `repoURL`, `runtime`).
- [ ] The runtime-specific config is present and correct:
  - **remote:** `remoteConfig.fixedURL`, and the endpoint is deployed and reachable.
  - **containerized:** `containerizedConfig.image` (public + pinned), `port`,
    `path` (and `healthzPath` if the server has one), and the image has been
    verified to run and answer on those paths.
- [ ] `entryKey` is unique across all entries in the catalog.
- [ ] A `docs/servers/<name>.md` page exists (for new servers).
- [ ] The README server table is updated.
- [ ] No secrets or credentials are included.

You can quickly check YAML validity locally, for example:

```bash
python -c "import yaml,sys; yaml.safe_load(open('my_server.yaml'))"
```

## Pull requests

- Keep each PR focused — one server per PR is the established convention (see
  the commit history).
- Use a descriptive commit message, e.g. `feat: add <Server Name> to catalog`.
- Note in the PR description that the endpoint has been verified as reachable.

## Questions

For questions about the catalog or the gateway, contact the GSA-TTS team
maintaining this repository.
