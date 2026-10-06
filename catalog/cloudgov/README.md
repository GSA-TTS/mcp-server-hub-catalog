# cloud.gov Catalog

This directory defines the MCP products published by the primary GSA cloud.gov
gateway. The repository-root `.obotcatalogs` selects only
`catalog/cloudgov/*.yaml` when Obot loads the `main` repository source.

## Architecture

Treat each migrated service as a pair in this directory:

- an `entry` describing the implementation-level `runtime: remote` component;
  and
- a launchable `type: vmcp` describing the user-facing product.

Users launch the vMCP. The component entry tells Obot how to reach the internal
application and can be composed by one or more vMCPs.

```text
MCP client
    |
    | public HTTPS + Obot OAuth or scoped API key
    v
Obot vMCP: /mcp-connect/<vmcp-id>
    |
    | private cloud.gov C2C policy
    v
MCP component: http://<app>.apps.internal:8080/mcp
```

The vMCP connection URL ends at `/mcp-connect/<vmcp-id>`. Do not append `/mcp`.

## Visibility And Access

| Layer | Exposure | Access control |
|---|---|---|
| MCP application | Private `apps.internal` route | cloud.gov C2C policy permits Obot on the application port |
| Component entry | Administrative implementation detail | Managed through the catalog; users do not launch it directly |
| vMCP endpoint | Publicly routable HTTPS endpoint | Obot OAuth or scoped API key plus vMCP profile authorization |

A public vMCP endpoint is not anonymously accessible. A profile with
`type: selector` and `id: "*"` grants access to all authenticated Obot users.

Keep each component and vMCP together in this source for atomic updates,
same-source references, predictable synchronization, and rollback. Keep the
component `entryKey`, vMCP `entryKey`, and component `id` stable.

Start with one vMCP per component. Add multi-component vMCPs only for coherent
user workflows; do not publish an unrestricted all-catalog vMCP by default.

## Migration Gate

Each migrated service must have:

- an `apps.internal` route and no public application route;
- a C2C policy allowing Obot to reach only the application port;
- a paired vMCP with explicit profiles and tool permissions;
- successful `/health`, `tools/list`, and real `tools/call` verification; and
- a successful connection from a real external MCP client using the exact vMCP
  URL.

## Legacy AWS Catalog

The `aws` branch preserves the containerized pilot catalog until cloud.gov
reaches parity. It remains supported for break/fix maintenance, but new servers
and product work target `main`. There are no production users on the AWS pilot.

## Repository Privacy

Never store credentials or secrets in either branch. Internal hostnames are not
credentials, but this public repository reveals service inventory and naming.
Obtain an explicit disclosure review before production or move the deployment
catalog to a private repository while keeping each component and vMCP together.
