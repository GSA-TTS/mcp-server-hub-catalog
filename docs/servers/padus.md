# NEPA USGS PAD-US MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The USGS PAD-US MCP server exposes the USGS Protected Areas Database of the
United States (PAD-US) as an MCP tool built for NEPA screening and baseline
analysis. Given a latitude/longitude and a buffer radius, it identifies PAD-US
protected-area records — designations and managing organizations — within a
region of interest (ROI), all through natural-language requests routed through
the obot MCP gateway.

- **Data source:** USGS PAD-US (Protected Areas Database of the United States)
  ArcGIS service.
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the PAD-US
  server is containerized additively under `docker/padus/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-usgs-padus` (`:8080/mcp`, health at
  `/health`). The container has no public route; it is reachable only through
  the gateway.
- **Authentication:** None required — queries the public USGS PAD-US service.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw ArcGIS
payloads:

- Results are returned as a Markdown summary of the PAD-US protected-area
  records intersecting the ROI, including the managing organization and
  designation.
- **Scope:** PAD-US is a protected-areas database, not a cadastral parcel or
  comprehensive land-ownership service.

## Tools

The server registers the following tool.

| Tool | Description |
|------|-------------|
| `get_padus_protected_areas_in_roi` | PAD-US protected-area designations and managing organizations within the ROI. |

## Parameters

### `get_padus_protected_areas_in_roi`

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "What protected areas are within 25 miles of 44.4, -110.6?"
- "Who manages the protected lands near latitude 37.7, longitude -119.5?"
- "Screen this site for PAD-US protected-area designations."

## References

- [USGS PAD-US (Protected Areas Database of the United States)](https://www.usgs.gov/programs/gap-analysis-project/science/pad-us-data-overview)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
