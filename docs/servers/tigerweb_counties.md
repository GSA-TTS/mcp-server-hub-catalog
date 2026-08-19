# NEPA Counties (TIGERweb) MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

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

- **Data source:** U.S. Census Bureau TIGERweb ArcGIS service.
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the server is
  containerized additively under `docker/tigerweb_counties/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-tigerweb-counties` (`:8080/mcp`, health at
  `/health`). The container has no public route; it is reachable only through
  the gateway.
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
