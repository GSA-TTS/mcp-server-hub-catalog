# BLM MLRS Geothermal Leases MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The BLM MLRS Geothermal Leases MCP server exposes the U.S. Bureau of Land
Management (BLM) [Mineral & Land Records System (MLRS)](https://mlrs.blm.gov/)
**Geothermal Leases** dataset as a set of MCP tools. The dataset is published as
an [Esri ArcGIS REST FeatureServer](https://gis.blm.gov/nlsdb/rest/services/HUB/BLM_Natl_MLRS_Geothermal_Leases/FeatureServer/0).

The server lets an AI application look up a single geothermal lease by its case
serial number, or search leases by state, status, and effective-/expiration-date
ranges, all through natural-language requests routed through the obot MCP
gateway.

- **Data source:** [BLM National MLRS Geothermal Leases FeatureServer](https://gis.blm.gov/nlsdb/rest/services/HUB/BLM_Natl_MLRS_Geothermal_Leases/FeatureServer/0)
- **Source repository:** [GSA-TTS/mcp-server-blm-mlrs](https://github.com/GSA-TTS/mcp-server-blm-mlrs)
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-blm-mlrs` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public BLM MLRS service.

## Design principles

The server returns clean, structured records rather than raw ArcGIS payloads:

- Queries request `returnGeometry=false` so responses stay small and
  context-window friendly.
- Only named `outFields` are returned (never `*` for search), keeping the
  response contract stable and minimal.
- Epoch-millisecond ArcGIS timestamps are normalized to ISO `YYYY-MM-DD` dates.
- Search results are capped at 50 records to keep responses bounded.

## Tools

The server registers the following tools.

| Tool | Description |
|------|-------------|
| `get_lease_details` | Retrieve full details for a single lease by its BLM case serial number — case name, lease type, status, state, acreage, commodity, formation, production status, and effective/expiration/sale dates. Returns an error if the case is not found. |
| `search_leases` | Search leases with optional filters (state, status, effective- and expiration-date ranges). All parameters are optional; if none are given, all leases are returned (capped at 50 records). Returns a count and a list of lease summaries. |

## Parameters

### `get_lease_details`

| Parameter | Description |
|-----------|-------------|
| `case_number` | BLM case serial number, e.g. `'NVNV105806473'`. |

### `search_leases`

All parameters are optional.

| Parameter | Field | Description |
|-----------|-------|-------------|
| `state` | `ADMIN_STATE` | Two-letter admin state code, e.g. `'NV'`. |
| `status` | `CSE_DISP` | Case disposition/status, e.g. `'Authorized'`. |
| `effective_date_from` | `EFF_DT` | Inclusive lower bound, ISO date `'YYYY-MM-DD'`. |
| `effective_date_to` | `EFF_DT` | Inclusive upper bound, ISO date `'YYYY-MM-DD'`. |
| `expiration_date_from` | `EXP_DT` | Inclusive lower bound, ISO date `'YYYY-MM-DD'`. |
| `expiration_date_to` | `EXP_DT` | Inclusive upper bound, ISO date `'YYYY-MM-DD'`. |

## Example prompts

- "Get details for BLM geothermal lease NVNV105806473"
- "Find authorized geothermal leases in Nevada"
- "List geothermal leases with an effective date in 2020"
- "Which geothermal leases in California expire before 2030?"

## References

- [BLM Mineral & Land Records System (MLRS)](https://mlrs.blm.gov/)
- [BLM National MLRS Geothermal Leases FeatureServer](https://gis.blm.gov/nlsdb/rest/services/HUB/BLM_Natl_MLRS_Geothermal_Leases/FeatureServer/0)
- [Source repository](https://github.com/GSA-TTS/mcp-server-blm-mlrs)
- [Model Context Protocol](https://modelcontextprotocol.io/)
