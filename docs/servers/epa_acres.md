# NEPA EPA ACRES MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The EPA ACRES MCP server exposes EPA's Assessment, Cleanup and Redevelopment
Exchange System (ACRES) Brownfields property records as an MCP tool built for
NEPA screening and contaminated-site redevelopment research. Given a
latitude/longitude and a buffer radius, it identifies grantee-reported
Brownfields properties within a region of interest (ROI), all through
natural-language requests routed through the obot MCP gateway.

- **Data source:** EPA ACRES via the public EPA Envirofacts facility-points
  ArcGIS service (Brownfields layer).
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the EPA ACRES
  server is containerized additively under `docker/epa_acres/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-epa-acres` (`:8080/mcp`, health at
  `/health`). The container has no public route; it is reachable only through
  the gateway.
- **Authentication:** None required — queries the public EPA Envirofacts service.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw ArcGIS
payloads:

- Results are returned as a Markdown summary of the ACRES Brownfields properties
  intersecting the ROI, grouped by state and paginated nearest-first.
- **Scope:** ACRES contains only properties reported through EPA Brownfields
  grant programs. It is not a complete inventory of brownfields or contaminated
  sites, and a record is not a determination that land is contaminated,
  available, or suitable for development.

## Tools

The server registers the following tool.

| Tool | Description |
|------|-------------|
| `get_epa_acres_properties_in_roi` | EPA ACRES grantee-reported Brownfields property records within the ROI. |

## Parameters

### `get_epa_acres_properties_in_roi`

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |
| `max_results` | Optional. Maximum records in this response, valid range 1 to 100 (default 100). |
| `result_offset` | Optional. Zero-based offset into records sorted nearest-first, valid range 0 to 9999 (default 0). |

## Example prompts

- "What Brownfields properties are within 25 miles of 39.95, -75.16?"
- "List EPA ACRES sites near latitude 42.36, longitude -71.06."
- "Screen this location for reported Brownfields redevelopment sites."

## References

- [EPA ACRES (Assessment, Cleanup and Redevelopment Exchange System)](https://www.epa.gov/cleanups/brownfields)
- [EPA Envirofacts](https://www.epa.gov/enviro)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
