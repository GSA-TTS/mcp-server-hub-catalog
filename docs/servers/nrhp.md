# NEPA NRHP MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The NRHP MCP server exposes the National Register of Historic Places (NRHP) as
an MCP tool built for Section 106 of the National Historic Preservation Act
(NHPA) and cultural-resource screening in NEPA analyses. Given a
latitude/longitude and a buffer radius, it identifies NRHP-listed historic
properties — including National Historic Landmarks (NHL) — within a region of
interest (ROI), all through natural-language requests routed through the obot
MCP gateway.

The data is served by the National Park Service Cultural Resources ArcGIS
MapServer.

- **Data source:** NPS Cultural Resources ArcGIS MapServer (National Register of
  Historic Places).
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the NRHP server
  is containerized additively under `docker/nrhp/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-nrhp` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public NPS service.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw ArcGIS
payloads:

- Results are returned as a Markdown summary of the NRHP-listed properties
  intersecting the ROI, oriented to Section 106 review.

## Tools

The server registers the following tool.

| Tool | Description |
|------|-------------|
| `get_nrhp_properties_in_roi` | NRHP-listed historic properties (including National Historic Landmarks) within the ROI, from the NPS Cultural Resources service. |

## Parameters

### `get_nrhp_properties_in_roi`

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "What historic properties are listed within 25 miles of 38.9, -77.0?"
- "Screen this site for NRHP properties near latitude 29.95, longitude -90.07."
- "Are there any National Historic Landmarks around this location?"

## References

- [National Register of Historic Places](https://www.nps.gov/subjects/nationalregister/index.htm)
- [Section 106 of the National Historic Preservation Act](https://www.achp.gov/protecting-historic-properties/section-106-process/introduction-section-106)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
