# Contributing to the MCP Server Hub Catalog

`main` is the primary cloud.gov catalog. The `aws` branch is the supported
legacy containerized pilot. Start every change from the branch that owns the
target deployment.

## Add a cloud.gov Service

Cloud.gov services use two manifests in `catalog/cloudgov/`.

### 1. Deploy the internal application

The MCP server must:

- listen on the Cloud Foundry-assigned application port;
- expose streamable HTTP at `/mcp` and health at `/health`;
- have only an `apps.internal` route; and
- have a C2C policy allowing the Obot app to reach only its application port.

Verify `/health` from inside the Obot container and confirm the equivalent
public `app.cloud.gov` route is unreachable.

### 2. Add the component entry

Create `catalog/cloudgov/<name>.yaml`:

```yaml
name: Example Internal
entryKey: obot-example
serverUserType: multiUser
shortDescription: Internal cloud.gov component for Example
repoURL: https://github.com/GSA-TTS/mcp-server-example
runtime: remote
remoteConfig:
  fixedURL: http://mcp-example.apps.internal:8080/mcp
```

Use an implementation-oriented display name. Users do not launch this entry.

### 3. Add the vMCP product

Create `catalog/cloudgov/<name>_vmcp.yaml`:

```yaml
type: vmcp
entryKey: example
displayName: Example
components:
  - id: example
    name: Example
    mcpServerCatalogEntryKey: obot-example
profiles:
  - name: everyone
    subjects:
      - type: selector
        id: "*"
    vmcpPermissions:
      allowedComponents:
        example:
          allowedTools: null
```

Profiles are authorization policy. `selector: "*"` means all authenticated
Obot users, not anonymous access. Prefer narrower subjects or tool allowlists
when the service does not need broad access.

Keep component `entryKey`, vMCP `entryKey`, and component `id` stable. Changing
them can disrupt reconciliation, saved configuration, and client connections.

### 4. Document and validate

Add or update `docs/servers/<name>.md`, the active table in `README.md`, and an
icon under `icons/` when needed.

The migration gate requires:

- valid YAML and unique keys;
- no legacy `env`, `remoteConfig.headers`, or
  `multiUserConfig.userDefinedHeaders` fields;
- internal-only routing and the expected C2C policy;
- `/health` from Obot;
- `tools/list` and a real `tools/call` through the gateway; and
- a successful OAuth or scoped-API-key connection from a real external client.

The client URL is `https://<obot-host>/mcp-connect/<vmcp-id>` with no `/mcp`
suffix.

## List an External Provider

An externally operated server is not an internal cloud.gov migration. FRED is
the explicit example: the official provider's `https://mcp.stlouisfed.org`
endpoint remains outside the GSA hub boundary even when proxied through Obot.

- Keep the remote component and paired vMCP under `catalog/cloudgov/`; use an
  implementation-oriented component name and a user-facing product name.
- Disclose the operator, external endpoint, boundary crossing, account
  requirements, and sensitive-input restrictions in both listings and docs.
- Use the exact provider endpoint. For per-user upstream authorization, declare
  `singleUser`; do not configure shared accounts, passwords, or manual tokens.
  Do not invent API-key fields when none are required.
- Use an explicit tool allowlist and document an external-service decision
  record. Review provider terms/privacy, data flows, and required egress before use.
- Verify live MCP initialization, authorization discovery, upstream OAuth,
  isolation across users, revocation/reauthorization, `tools/list`, real tool
  calls, external-client access, and unauthenticated rejection. Internal-app
  routing/C2C and `/health` checks do not apply to an external provider.
- Track blocked acceptance in the service document or feature issue/PR and
  never describe static validation as a live integration pass.

Listing does not approve a provider for production or sensitive government
data. Deployment, egress, or authentication changes require separate approval.
See [FRED](docs/servers/fred.md) for the current blocked acceptance record.

## Maintain the AWS Pilot

AWS break/fix changes start from `aws`. That branch retains one containerized
entry per server at the repository root. Container images must remain public,
version-pinned, and compatible with `linux/amd64`.

Do not add new products to AWS unless required to maintain pilot parity. New
services target cloud.gov on `main`.

## Field Conventions

See [`docs/SCHEMA.md`](docs/SCHEMA.md) for the generic entry and vMCP schema.

- Never commit credentials, tokens, or secret values.
- User-supplied environment values use top-level `config` entries with
  `usage: env`; current Obot rejects legacy `env`.
- Keep one service migration per PR.
- Branch from an up-to-date `main` for cloud.gov or `aws` for legacy fixes.
- Include verification, rollback, security impact, and AI assistance in the PR.
- Do not self-merge; require human review and passing CI.
