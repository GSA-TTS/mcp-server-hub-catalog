# NEPA Tribal Lands MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.
>
> **Migration status (2026-10-20):** the digest-pinned Tribal Lands application
> passed cloud.gov startup, internal-only route metadata, port-scoped C2C policy,
> gateway-to-`/health` reachability, and the supplemental public HTTP negative
> probe. Catalog synchronization, authenticated vMCP `tools/list`, a real
> `tools/call`, and external-client verification remain pending.

## Overview

The Tribal Lands MCP server exposes tribal-land geographic context as an MCP
tool built for NEPA early-coordination and project-area review. Given a
latitude/longitude and a buffer radius, it identifies American Indian / Alaska
Native / Native Hawaiian Areas (AIANNHA) that intersect a region of interest
(ROI), all through natural-language requests routed through the obot MCP
gateway.

- **Data source:** U.S. Census Bureau TIGERweb AIANNHA ArcGIS service.
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the Tribal Lands
  server is containerized additively under `docker/tribal/`).
- **Runtime:** an internal cloud.gov application registered as a `remote`
  component and exposed to users through the NEPA Tribal Lands vMCP. A
  port-scoped C2C policy permits the gateway to reach `:8080/mcp`; the
  application has no public route.
- **Client access:** authenticated through the gateway at
  `/mcp-connect/<vmcp-id>` with no `/mcp` suffix.
- **Authentication:** None required — queries the public Census service.

## Scope and limitations

This server returns the Census TIGERweb AIANNHA **cartographic boundary** layer.
It provides *geographic context* for a project area — it is **not** the
authoritative basis for government-to-government tribal consultation, and a
no-hit result does not establish the absence of tribal interests. Use it to
orient early coordination, not to satisfy a consultation obligation.

## Tools

The server registers the following tool.

| Tool | Description |
|------|-------------|
| `get_tribal_lands_in_roi` | Tribal lands (AIANNHA areas) intersecting the ROI, from Census TIGERweb. |

## Parameters

### `get_tribal_lands_in_roi`

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "What tribal lands are within 25 miles of 35.68, -105.94?"
- "Are there any AIANNHA areas near latitude 43.6, longitude -102.5?"
- "Screen this site for tribal-land geographic context."

## References

- [Census TIGERweb](https://tigerweb.geo.census.gov/tigerwebmain/TIGERweb_main.html)
- [American Indian/Alaska Native/Native Hawaiian Areas (AIANNHA)](https://www.census.gov/programs-surveys/geography/guidance/geo-areas/aian-areas.html)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
