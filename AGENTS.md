# AGENTS.md — MCP Server Hub Catalog

This project-level contract supplements the universal agent rules.

## Branch Roles

- `main` is the primary cloud.gov catalog.
- `aws` is the supported legacy containerized pilot.
- New services and migrations target `main`.
- AWS break/fix maintenance targets `aws` and is not merged into `main` unless
  it also applies to cloud.gov.

## Canonical References

- [`CONTRIBUTING.md`](CONTRIBUTING.md): workflow and verification gates.
- [`catalog/cloudgov/README.md`](catalog/cloudgov/README.md): deployment
  architecture and visibility model.
- [`docs/SCHEMA.md`](docs/SCHEMA.md): generic field reference.

If these documents disagree on field syntax, `docs/SCHEMA.md` wins. If they
disagree on deployment architecture, `catalog/cloudgov/README.md` wins.

## Main Branch Rules

- Add cloud.gov manifests only under `catalog/cloudgov/`.
- Every service has a `runtime: remote` component and a `type: vmcp` product.
- Component names should identify them as internal implementation details.
- Users launch/connect to vMCPs, not component entries.
- Internal apps use `apps.internal`, no public application route, and a
  port-scoped C2C policy from Obot.
- The external Obot endpoint is `/mcp-connect/<vmcp-id>` without `/mcp`.
- Keep component/vMCP identifiers stable.
- Do not create unrestricted aggregate vMCPs without a concrete workflow.

## AWS Branch Rules

- Preserve root containerized entries and existing behavior.
- Accept break/fix, security, dependency-pin, and compatibility maintenance.
- Do not add speculative functionality or new products.
- Verify images are public, version-pinned, and `linux/amd64`.

## Security And Verification

- Never commit credentials, API keys, tokens, or secret values.
- Treat internal hostnames as sensitive architecture metadata even though they
  are not credentials.
- User configuration uses top-level `config`; legacy `env` is invalid.
- Validate YAML, unique keys, component references, profiles, and tool policy.
- A cloud.gov migration requires live `/health`, `tools/list`, `tools/call`, and
  external-client verification.
- Document AI assistance and require human review before merge.
