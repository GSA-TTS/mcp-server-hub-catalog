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

1. **Confirm the server is deployed and reachable.** The gateway connects to a
   fixed remote endpoint (typically a cloud.gov `/mcp` URL). Verify the endpoint
   responds before adding it to the catalog.

2. **Create the entry file.** Add a new file named `<name>.yaml` in
   `snake_case` at the repository root. At minimum it must contain the required
   fields:

   ```yaml
   name: my_server
   entryKey: obot-my-server
   serverUserType: singleUser
   shortDescription: Access data from the Example API
   repoURL: https://github.com/GSA-TTS/mcp-server-my-server
   runtime: remote
   remoteConfig:
     fixedURL: https://my-server-mcp-server.app.cloud.gov/mcp
   ```

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
- Use `serverUserType: singleUser` unless the server is designed for
  multi-user/shared authentication.
- Never commit secrets, API keys, or credentials in a catalog entry. Catalog
  entries describe **how to connect**, not **how to authenticate with private
  credentials**.

## Validation checklist

Before opening a pull request, confirm:

- [ ] The file is valid YAML (no tabs, correct indentation).
- [ ] All required fields are present (`name`, `entryKey`, `serverUserType`,
      `shortDescription`, `repoURL`, `runtime`, `remoteConfig.fixedURL`).
- [ ] `entryKey` is unique across all entries in the catalog.
- [ ] The `fixedURL` endpoint is deployed and reachable.
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
