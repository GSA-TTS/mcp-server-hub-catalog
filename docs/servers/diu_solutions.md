---
title: DIU Solutions Catalog MCP Server
description: Public DIU catalog snapshot discovery through a private cloud.gov component and authenticated vMCP.
status: draft
tier: 2
last_updated: 2026-11-09
related_files: [catalog/cloudgov/diu_solutions.yaml, catalog/cloudgov/diu_solutions_vmcp.yaml, README.md, CONTRIBUTING.md]
---

# DIU Solutions Catalog MCP Server

> **Status:** Pilot / proof of concept. Not authorized for production use.
> Cloud.gov application running; C2C, gateway, and external-client verification pending.

## Purpose and source

This service makes successful DIU prototypes easier to discover by mission need,
capability, vendor, focus area, and completion year. It packages a point-in-time
snapshot of the public [DIU Commercial Solutions Catalog](https://www.diu.mil/solutions/portfolio/catalog),
not a live DIU API proxy. The snapshot does not refresh automatically.

- **Source fork:** [GSA-TTS/mcp-diu-solutions-catalog](https://github.com/GSA-TTS/mcp-diu-solutions-catalog)
- **Deployment kit:** [Docker cloud.gov runbook](https://github.com/GSA-TTS/mcp-diu-solutions-catalog/blob/main/deploy/cloudgov/README.md)
- **Component:** [DIU Solutions Catalog Internal](../../catalog/cloudgov/diu_solutions.yaml)
- **Product:** [DIU Solutions Catalog vMCP](../../catalog/cloudgov/diu_solutions_vmcp.yaml)

The image includes the CSV snapshot, local `BAAI/bge-small-en-v1.5` embedding
model, and embedded Qdrant index. Semantic search runs locally. The deployed
local-model build uses offline model loading; ordinary startup does not scrape
DIU or rebuild the index. One worker owns each instance's local Qdrant files.

## Access and deployment

The private component is reached at
`http://mcp-diu-solutions.apps.internal:8001/mcp`, with liveness at `/health` and
readiness at `/ready`. Unlike the other catalog examples, this app uses **8001**.
It has no mapped public application route in the operator-provided route evidence.

The required C2C policy permits only the approved Obot source app to reach the
DIU application on TCP port 8001. This policy and health/readiness from Obot
must be verified before treating the listing as ready for users.

Users connect through Obot OAuth or a scoped API key:

```text
https://<obot-host>/mcp-connect/<actual-vmcp-id>
```

Obot supplies the actual vMCP ID after reconciliation; do not assume it equals
the `diu-solutions` entry key. Do not append `/mcp`.

The `everyone` profile authorizes all **authenticated** Obot users, not anonymous
clients, and explicitly allows the six tools below. The underlying server also
defines `catalog_status`, which returns local paths; it is excluded from this
product's allowlist and preview. Verify that it is denied/not advertised to the
normal product audience. No user-supplied upstream credentials are required.

## Tools

| Tool | Purpose | Parameters |
|---|---|---|
| `search_solutions` | Semantic discovery with full public records and similarity scores | `query`; optional `limit`, exact `portfolio`, `vendor`, `year_completed` |
| `get_solution` | Exact record retrieval | `uuid` |
| `list_solutions` | Browse with exact filters and pagination | Optional `portfolio`, `vendor`, `year_completed`, `limit`, `offset` |
| `catalog_facets` | Available filter values and counts | None |
| `search` | Citation-friendly semantic results | `query` |
| `fetch` | Citation-ready content for a search result | `id` |

All tools are read-only. Use `catalog_facets` to obtain exact filter values.
Use a UUID from `search_solutions` with `get_solution`, or an ID from `search`
with `fetch`. Public record payloads exclude raw HTML and scrape timestamps.

## Example prompts and limitations

- "Find solutions for resilient communications in disconnected environments."
- "Which projects address autonomous maritime capabilities?"
- "List available focus areas, then show projects in one of those areas."
- "Retrieve the full DIU record and source citation for this search result."

Similarity scores describe text relevance, not effectiveness, maturity, eligibility,
endorsement, or procurement suitability. Verify important information against
canonical DIU URLs. Snapshot coverage and counts can change with refreshes.
Do not submit sensitive mission details to a pilot solely because the indexed
catalog data is public.

## Verification evidence and remaining gates

Operator-provided evidence on 2026-11-09 confirms:

- Offline Docker startup and restart: `/health`, `/ready`, matching nonempty
  CSV/index counts, and real calls to all six product tools passed.
- Published image inspected as `linux/amd64` and cloud.gov app running 1/1.
- Only the intended internal route mapped, with application port 8001.
- Deployed platform manifest:
  `ghcr.io/gsa-tts/mcp-diu-solutions-catalog@sha256:9ed2e288952493c82aca4adb5dda23e397a0a0e7e285ae4dbcad396b3a191982`.

Not yet verified in this catalog addition:

- YAML/schema validation, unique keys, component references, and Obot acceptance
  of the explicit tool allowlist.
- Port-scoped C2C policy and health/readiness from inside Obot; unauthorized
  source apps denied and no public app route reachable.
- Catalog reconciliation, gateway `tools/list`, real search/retrieval calls,
  and `catalog_status` restriction.
- Intended real external MCP client connection with OAuth or a scoped API key.

Retain pending status until all gates pass. The existing `/ready` can return raw
exception details on failure; keep diagnostics private. Sanitization is outside
this deployment/listing scope and requires a separate development-team proposal.

## Change review and rollback

This listing was prepared with AI assistance and requires human review. No
production authorization or successful gateway verification is implied.
Follow [CONTRIBUTING.md](../../CONTRIBUTING.md) for verification and PR disclosure.

Rollback the component/product pair together using a reviewed catalog revert
and reconciliation. Preserve stable entry keys and component IDs. Application
rollback selects a previous verified image digest using the isolated deployment
kit; it does not rebuild the running index in place. Keep deployment credentials
and private verification logs out of catalog files and public PR artifacts.
