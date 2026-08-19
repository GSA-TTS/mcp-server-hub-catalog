# NEPA EFH MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The EFH MCP server exposes NOAA Essential Fish Habitat (EFH) data as a set of
MCP tools built for Magnuson-Stevens Act compliance and ESA Section 7
consultation screening in NEPA analyses. Given a latitude/longitude and a buffer
radius, it screens a region of interest (ROI) against EFH, Habitat Areas of
Particular Concern (HAPC), and species-group EFH — all through natural-language
requests routed through the obot MCP gateway.

The datasets are published as
[Esri ArcGIS REST services](https://www.habitat.noaa.gov/) by the NOAA
Fisheries West Coast Region.

- **Data source:** NOAA Fisheries West Coast Region Essential Fish Habitat
  ArcGIS services.
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the EFH server
  is containerized additively under `docker/efh/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-efh` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public NOAA EFH services.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw ArcGIS
payloads:

- Each tool returns a Markdown summary of the designations intersecting the ROI.
- For HMS/CPS/Groundfish, polygon acreage is unioned by designation and clipped
  to the requested point-buffer ROI; source feature acreage is retained
  separately.
- **Coverage:** the underlying services are NOAA Fisheries West Coast Region
  EFH. Outside that geography, no hits may simply mean out-of-scope rather than
  absence of habitat.

## Tools

The server registers the following tools.

| Tool | Description |
|------|-------------|
| `get_efh_hapc` | Habitat Areas of Particular Concern (HAPC) within the ROI — high-priority EFH subsets warranting heightened Magnuson-Stevens Act scrutiny. |
| `get_efh_areas` | General Essential Fish Habitat areas within the ROI — waters and substrate necessary for fish spawning, breeding, feeding, or growth to maturity. |
| `get_efh_salmon` | Salmon EFH by HUC-8 watershed within the ROI — Chinook, Coho, and Pink salmon, identifying which species apply per watershed. |
| `get_efh_hms_cps_groundfish` | HMS, Coastal Pelagic Species, and Pacific Coast Groundfish EFH within the ROI, with acreage unioned by designation and clipped to the ROI. |

## Parameters

All four tools take the same parameters.

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "Are there any Habitat Areas of Particular Concern within 25 miles of 47.6, -124.4?"
- "What Essential Fish Habitat is near latitude 46.2, longitude -124.0?"
- "Which salmon species have EFH watersheds around this site?"
- "Screen this location for HMS, coastal pelagic, and groundfish EFH."

## References

- [NOAA Essential Fish Habitat](https://www.fisheries.noaa.gov/national/habitat-conservation/essential-fish-habitat)
- [Magnuson-Stevens Fishery Conservation and Management Act](https://www.fisheries.noaa.gov/topic/laws-policies/magnuson-stevens-act)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
