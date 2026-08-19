# NEPA FEMA NFHL MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The NEPA FEMA NFHL MCP server exposes the Federal Emergency Management Agency
[National Flood Hazard Layer (NFHL)](https://www.fema.gov/flood-maps/national-flood-hazard-layer)
as a set of MCP tools built for NEPA/EIS flood-hazard screening. Given a
latitude/longitude and a search radius, it screens a region of interest (ROI)
against mapped flood zones, levees, and water areas — all through
natural-language requests routed through the obot MCP gateway.

> **Not to be confused with** the separate standalone
> [FEMA NFHL](fema_nfhl.md) catalog entry
> ([GSA-TTS/mcp-server-fema-nfhl](https://github.com/GSA-TTS/mcp-server-fema-nfhl),
> image `ghcr.io/gsa-tts/mcp-server-fema-nfhl`). This entry is the NEPA fork's
> flood-hazard-screening server, published as
> `ghcr.io/gsa-tts/mcp-server-nepa-fema-nfhl` with the `nepa-` prefix to
> disambiguate. The two expose different tool sets.

- **Data source:** [FEMA National Flood Hazard Layer ArcGIS REST service](https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer)
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the FEMA NFHL
  server is containerized additively under `docker/fema_nfhl/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-fema-nfhl` (`:8080/mcp`, health at
  `/health`). The container has no public route; it is reachable only through
  the gateway.
- **Authentication:** None required — queries the public FEMA NFHL service.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw ArcGIS
payloads:

- Each tool returns a Markdown summary of the flood-hazard features intersecting
  the ROI.
- The screening tool combines flood zones, levees, and water areas into a single
  overview for a one-shot NEPA flood-hazard screen.

## Tools

The server registers the following tools.

| Tool | Description |
|------|-------------|
| `get_fema_nfhl_flood_zones_in_roi` | FEMA flood hazard zone classifications (Zone A, AE, X, D, etc.) within the ROI. |
| `get_fema_nfhl_levees_in_roi` | FEMA-mapped levee locations within the ROI. |
| `get_fema_nfhl_water_areas_in_roi` | Water areas (rivers, lakes, etc.) within the ROI. |
| `analyze_fema_nfhl_flood_hazard_screening` | One-shot screening combining flood zones, levees, and water areas. |

## Parameters

All four tools take the same parameters.

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `radius_miles` | Optional. Search radius in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "Is 29.9511, -90.0715 in a FEMA flood zone within 5 miles?"
- "Are there any FEMA-mapped levees near latitude 38.6, longitude -90.2?"
- "What water areas are within 10 miles of this site?"
- "Run a FEMA NFHL flood-hazard screening for this location."

## References

- [FEMA National Flood Hazard Layer](https://www.fema.gov/flood-maps/national-flood-hazard-layer)
- [FEMA NFHL ArcGIS REST service](https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
