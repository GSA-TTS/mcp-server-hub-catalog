# NEPA GBIF MCP Server

> **Status:** Pilot / proof of concept. Not intended for production use.

## Overview

The GBIF MCP server exposes the Global Biodiversity Information Facility
[(GBIF)](https://www.gbif.org/) as a set of MCP tools built for NEPA/EIS
biodiversity screening. Given a latitude/longitude and a buffer radius, it
returns georeferenced species occurrence records — actual observation
coordinates — and county-level species presence within a region of interest
(ROI), all through natural-language requests routed through the obot MCP
gateway.

Unlike species-list sources (e.g. USFWS IPaC), GBIF provides the observed
lat/lon for each record, so sightings can be mapped and habitat-use patterns
analyzed.

- **Data sources:**
  - [GBIF API](https://www.gbif.org/developer/summary) — georeferenced species
    occurrences.
  - Census county ArcGIS service — for county-level aggregation.
- **Source repository:** [GSA-TTS/nepa-mcp](https://github.com/GSA-TTS/nepa-mcp)
  (a fork of [pnnl/nepa-mcp](https://github.com/pnnl/nepa-mcp); the GBIF server
  is containerized additively under `docker/gbif/`).
- **Runtime:** `containerized` — hosted by the gateway from the public image
  `ghcr.io/gsa-tts/mcp-server-nepa-gbif` (`:8080/mcp`, health at `/health`).
  The container has no public route; it is reachable only through the gateway.
- **Authentication:** None required — queries the public GBIF API.

## Design principles

The server returns compact, decision-oriented **evidence**, not raw GBIF
payloads:

- Occurrence results carry the observed coordinates and are filtered to
  threatened/endangered species and a minimum year by default, bounded by a
  record cap.
- County aggregation reports species presence per county for NEPA/EIS reporting.

## Tools

The server registers the following tools.

| Tool | Description |
|------|-------------|
| `get_gbif_species_occurrences_in_roi` | Georeferenced species occurrences (actual lat/lon) within the ROI, for mapping sightings and habitat-use analysis. |
| `get_gbif_species_list_by_county` | Species presence aggregated by county within the ROI buffer, for county-level NEPA/EIS reporting. |

## Parameters

Both tools share the geospatial and filter parameters; they differ only in the
record-cap parameter name.

| Parameter | Description |
|-----------|-------------|
| `latitude` | Latitude in decimal degrees (WGS84), valid range -90 to 90. |
| `longitude` | Longitude in decimal degrees (WGS84), valid range -180 to 180. |
| `buffer_miles` | Optional. Buffer distance in miles, valid range 0.1 to 100.0 (default 25). |
| `threatened_only` | Optional. Only return threatened/endangered species (default true). |
| `min_year` | Optional. Minimum observation year (default 2015). |
| `max_records` / `max_records_per_county` | Optional. Record cap, valid range 1 to 5000 (default 1000). `max_records` for the occurrences tool; `max_records_per_county` for the by-county tool. |

## Example prompts

- "What threatened species have been observed within 25 miles of 44.4, -110.6?"
- "List species presence by county near latitude 34.05, longitude -118.24."
- "Show all GBIF occurrences (not just threatened) since 2010 around this site."

## References

- [GBIF](https://www.gbif.org/)
- [GBIF API documentation](https://www.gbif.org/developer/summary)
- [Source repository](https://github.com/GSA-TTS/nepa-mcp)
- [Upstream project (PNNL)](https://github.com/pnnl/nepa-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
