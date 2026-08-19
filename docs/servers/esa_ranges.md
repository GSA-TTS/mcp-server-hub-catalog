# NEPA ESA Ranges MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The ESA Ranges MCP server exposes NOAA ESA-listed species range data as an MCP
tool built for Endangered Species Act (ESA) Section 7 consultation screening in
NEPA analyses. Given a latitude/longitude and a buffer radius, it identifies
ESA-listed salmon and steelhead ranges — with HUC-12 watershed detail — that
intersect a region of interest (ROI), all through natural-language requests
routed through the obot MCP gateway.

The data is published as an
[Esri ArcGIS REST FeatureServer](https://www.fisheries.noaa.gov/) (the NOAA
Fisheries West Coast Region Ranges_dice service).

- **Data source:** NOAA Fisheries West Coast Region Ranges_dice ArcGIS
  FeatureServer (ESA-listed species ranges).
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the ESA Ranges
  server is containerized additively under `docker/esa_ranges/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-esa-ranges` (`:8080/mcp`, health at
  `/health`). The container has no public route; it is reachable only through
  the gateway.
- **Authentication:** None required — queries the public NOAA service.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw ArcGIS
payloads:

- Results are returned as a Markdown summary of the ESA range records
  intersecting the ROI, broken down by HUC-12 watershed.
- Watershed polygons are unioned by range record and clipped to the requested
  point-buffer ROI; upstream whole-watershed area is retained separately for
  provenance.
- **Coverage:** the underlying service is NOAA Fisheries West Coast Region.
  Outside that geography, a no-hit result may mean out-of-scope rather than no
  ESA concern.

## Tools

The server registers the following tool.

| Tool | Description |
|------|-------------|
| `get_esa_species_ranges_in_roi` | ESA-listed species ranges within the ROI — salmon and steelhead range records from the NOAA Fisheries West Coast Region, broken down by HUC-12 watershed and clipped to the ROI. |

## Parameters

### `get_esa_species_ranges_in_roi`

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "What ESA-listed species ranges are within 25 miles of 45.5, -122.6?"
- "Are there ESA salmon or steelhead ranges near latitude 47.6, longitude -122.3?"
- "Screen this site for ESA species ranges by watershed."

## References

- [NOAA Fisheries — Endangered Species Conservation](https://www.fisheries.noaa.gov/topic/endangered-species-conservation)
- [ESA Section 7 Consultation](https://www.fisheries.noaa.gov/national/endangered-species-conservation/consultations)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
