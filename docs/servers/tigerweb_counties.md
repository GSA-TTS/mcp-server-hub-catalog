# NEPA Counties (TIGERweb) MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.
>
> **Migration verification (2026-10-20):** the digest-pinned TIGERweb Counties
> application passed cloud.gov startup, internal-only route metadata,
> port-scoped C2C policy, gateway-to-`/health` reachability, and the supplemental
> public HTTP negative probe. The catalog synchronized, the NEPA Counties
> (TIGERweb) vMCP launched, and authenticated `tools/list`, a real `tools/call`,
> and an external MCP client connection all passed.

## Overview

The TIGERweb Counties MCP server exposes county discovery as an MCP tool built
for jurisdictional coordination and permitting analysis in NEPA reviews. Given a
latitude/longitude and a buffer radius, it identifies every county that
intersects a region of interest (ROI), all through natural-language requests
routed through the obot MCP gateway.

> **Boundary lookup vs. statistics:** this server answers "which counties
> overlap this area?" using the Census TIGERweb boundary service. For
> county-level socioeconomic statistics (income, poverty, employment), use the
> separate [Census](census.md) (ACS) server.
> County intersection also does not establish legal jurisdiction, agency
> authority, consultation responsibility, or a permitting determination.

- **Data source:** U.S. Census Bureau TIGERweb ArcGIS service.
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the server is
  containerized additively under `docker/tigerweb_counties/`).
- **Runtime:** an internal cloud.gov application registered as a `remote`
  component and exposed to users through the NEPA Counties (TIGERweb) vMCP. A
  port-scoped C2C policy permits the gateway to reach `:8080/mcp`; the
  application has no public route.
- **Client access:** authenticated through the gateway at
  `/mcp-connect/<vmcp-id>` with no `/mcp` suffix.
- **Authentication:** None required — queries the public Census service.

## Tools

The server registers the following tool.

| Tool | Description |
|------|-------------|
| `get_tigerweb_counties_in_roi` | All counties intersecting the ROI buffer, with names and FIPS identifiers, from Census TIGERweb. |

## Parameters

### `get_tigerweb_counties_in_roi`

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "What counties are within 25 miles of 39.06, -108.55?"
- "Which counties intersect a 10-mile buffer around latitude 34.05, longitude -118.24?"
- "List the counties for this project area for jurisdictional coordination."

## References

- [Census TIGERweb](https://tigerweb.geo.census.gov/tigerwebmain/TIGERweb_main.html)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
