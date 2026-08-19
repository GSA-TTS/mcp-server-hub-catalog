# NEPA IPaC MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The IPaC MCP server exposes the U.S. Fish & Wildlife Service
[Information for Planning and Consultation (IPaC)](https://ipac.ecosphere.fws.gov/)
as an MCP tool built for Endangered Species Act (ESA) Section 7 consultation and
biological-resource screening in NEPA analyses. Given a latitude/longitude and a
buffer radius, it returns the USFWS trust resources — ESA-listed species,
migratory birds, wetlands, critical habitat, and National Wildlife Refuges —
that fall within a region of interest (ROI), all through natural-language
requests routed through the obot MCP gateway.

- **Data source:** [USFWS Information for Planning and Consultation (IPaC)](https://ipac.ecosphere.fws.gov/)
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the IPaC server
  is containerized additively under `docker/ipac/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-ipac` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public USFWS IPaC service.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw IPaC
payloads:

- A single call screens the ROI across all IPaC resource categories and returns
  a Markdown summary.
- Complements GBIF (georeferenced occurrences) and ESA Ranges (range polygons):
  IPaC provides the authoritative USFWS trust-resource list for Section 7.

## Tools

The server registers the following tool.

| Tool | Description |
|------|-------------|
| `get_ipac_resources_in_roi` | ESA-listed species, migratory birds, wetlands, critical habitat, and National Wildlife Refuge data within the ROI, as a Markdown summary. |

## Parameters

### `get_ipac_resources_in_roi`

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |

## Example prompts

- "What USFWS-listed species and critical habitat are within 25 miles of 38.9, -77.0?"
- "Screen this site for migratory birds and wetlands near latitude 30.3, longitude -97.7."
- "Are there any National Wildlife Refuges around this location?"

## References

- [USFWS Information for Planning and Consultation (IPaC)](https://ipac.ecosphere.fws.gov/)
- [ESA Section 7 Consultation](https://www.fws.gov/service/section-7-consultation)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
