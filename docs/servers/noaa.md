# NEPA NOAA Critical Habitat MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The NOAA MCP server exposes NOAA Fisheries West Coast Region ESA-designated
critical habitat as an MCP tool built for Endangered Species Act (ESA) Section 7
consultation screening in NEPA analyses. Given a latitude/longitude and a buffer
radius, it identifies designated critical habitat (lines and polygons) that
intersects a region of interest (ROI), all through natural-language requests
routed through the obot MCP gateway.

The data is published as an
[Esri ArcGIS REST FeatureServer](https://www.fisheries.noaa.gov/) by NOAA
Fisheries (West Coast Region).

- **Data source:** NOAA Fisheries West Coast Region ESA critical-habitat ArcGIS
  FeatureServer.
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the NOAA server
  is containerized additively under `docker/noaa/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-noaa` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public NOAA service.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw ArcGIS
payloads:

- Results are returned as a Markdown summary of the critical-habitat features
  intersecting the ROI.
- Polygon area is unioned across diced fragments and clipped to the requested
  point-buffer ROI; upstream whole-feature area is retained separately for
  provenance.
- **Coverage:** the underlying service is NOAA Fisheries West Coast Region.
  Outside that geography, a no-hit result may mean out-of-scope rather than no
  ESA concern.

## Related servers

This server covers NOAA-managed **critical habitat**. For related NEPA
biological screening see also the NEPA ESA Ranges server (ESA-listed species
ranges), NEPA EFH (essential fish habitat), NEPA IPaC (USFWS trust resources),
and NEPA GBIF (georeferenced occurrences).

## Tools

The server registers the following tool.

| Tool | Description |
|------|-------------|
| `get_noaa_critical_habitat_in_roi` | NOAA West Coast Region ESA-designated critical habitat (salmon, steelhead, marine mammals, marine fish) intersecting the ROI, clipped to the ROI. |

## Parameters

### `get_noaa_critical_habitat_in_roi`

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "Is there NOAA critical habitat within 25 miles of 45.5, -122.6?"
- "Screen this site for ESA critical habitat near latitude 47.6, longitude -122.3."
- "What NOAA-managed species have critical habitat around this location?"

## References

- [NOAA Fisheries — Critical Habitat](https://www.fisheries.noaa.gov/national/endangered-species-conservation/critical-habitat)
- [ESA Section 7 Consultation](https://www.fisheries.noaa.gov/national/endangered-species-conservation/consultations)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
